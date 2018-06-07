#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <stdlib.h>
#include <time.h>

int processID;
int logicClock = 1;
int n;
int pipelines[20][2];
int waitingResponses[20];
char receiveBuffer[30];
char sendBuffer[30];

void sendResponseMessage(int i, int clock)
{
    sprintf(sendBuffer, "%s(%d,%2d)", "Odgovor", processID, clock);
    printf("Filozof %d salje %s filozofu %d.\n", processID, sendBuffer, i);
    write(pipelines[i][1], sendBuffer, strlen(sendBuffer) + 1);
}

void sendRequests()
{
    int i=0;
    for (i = 0; i < n; i++)
    {
        if (i == processID)
        {
            continue;
        }
        sprintf(sendBuffer, "%s(%d,%2d)", "Zahtjev", processID, logicClock);
        printf("Filozof %d salje %s filozofu %d.\n", processID, sendBuffer, i);
        write(pipelines[i][1], sendBuffer, strlen(sendBuffer) + 1);
    }
}



void receiveReqsAndResps()
{
    int otherProcessID, otherProcessClock;
    int requestClock = logicClock;
    int nOfResponses=0;
    while(1)
    {
        int nread=read(pipelines[processID][0], receiveBuffer, 14);
        if(nread<=0)
        {
            usleep(100000);
            continue;
        }
        sscanf(receiveBuffer, "%*7s(%d, %d)", &otherProcessID, &otherProcessClock);
        printf("Filozof %d primio %s.\n", processID, receiveBuffer);
        if(logicClock>=otherProcessClock)
        {
            logicClock++;
        }
        else
        {
            logicClock=otherProcessClock+1;
        }
        if(receiveBuffer[0]=='O')
        {
            nOfResponses++;
            if(nOfResponses==n-1)
            {
                break;
            }
            else
            {
                continue;
            }
        }
        if ((requestClock == otherProcessClock && processID < otherProcessID)||(requestClock < otherProcessClock))
        {
            waitingResponses[otherProcessID] = otherProcessClock;
        }
        else
        {
            sendResponseMessage(otherProcessID, otherProcessClock);
        }
    }
}

void recvRestReqs()
{
    int otherProcessID, otherProcessClock;
    while(1)
    {
        int nread=read(pipelines[processID][0], receiveBuffer, 14);
        if(nread<=0)
        {
            break;
        }
        sscanf(receiveBuffer, "%*7s(%d, %d)", &otherProcessID, &otherProcessClock);
        printf("Filozof %d primio %s.\n", processID, receiveBuffer);
        if(logicClock>=otherProcessClock)
        {
            logicClock++;
        }
        else
        {
            logicClock=otherProcessClock+1;
        }
        sendResponseMessage(otherProcessID, otherProcessClock);
    }
}


void sendResponses()
{
    int i=0;
    for (i = 0; i < n; i++)
    {
        if (i == processID)
        {
            continue;
        }
        if (waitingResponses[i])
        {
            sendResponseMessage(i, waitingResponses[i]);
            waitingResponses[i] = 0;
        }
    }
}

void process()
{
    int i=0;
    for (i = 0; i < n; i++)
    {
        if (i == processID)
        {
            continue;
        }
        close(pipelines[i][0]);
    }
    close(pipelines[processID][1]);
    srand((unsigned)time(NULL)^processID);
    int sleeping=rand()%1500000;
    usleep(sleeping);
    recvRestReqs();
    while(1)
    {
        sendRequests();
        receiveReqsAndResps();
        //kriticni odsjecak
        printf("Filozof %d je za stolom.\n\n", processID);
        sleep(1);
        logicClock++;

        sendResponses();
        int i=0;
        int nTime=rand()%15;
        for(i=0; i<nTime; i++)
        {
            recvRestReqs();
            usleep(rand()%300000);
        }
    }
}


int main(int argc,char * argv[])
{
    if(argc!=2)
    {
        printf("Error!\n");
    }
    int i=0;
    n=atoi(argv[1]);
    if(n<=2)
    {
        printf("N of proccesses must be greater than 2!");
        exit(0);
    }
    for (i = 0; i < n; i++)
    {
        pipe(pipelines[i]);
        fcntl(pipelines[i][0], F_SETFL, O_NONBLOCK);
    }
    for(i=0; i<n; i++)
    {
        switch(fork())
        {
        case -1:
            printf("nest ne valja\n");
            break;
        case 0:
            processID = i;
            process();
            exit(0);
        }
    }

    for(i=0; i<n; i++)
    {
        wait(NULL);
    }

    exit(0);
}
