using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using MPI;
using System;
using System.Timers;


namespace NOS_lab1
{

    class Program
    {
        static int processId;
        static int M;
        static long LOAD_TIME = 4000;
        static int N;
        public const string identation = "                    ";
        static void Main(string[] args)
        {
            using (new MPI.Environment(ref args))
            {
                Intracommunicator comm = Communicator.world;
                processId = comm.Rank;
                if (args.Length != 2)
                {
                    if (processId == 0)
                    {
                        Console.WriteLine("Potrebna su dva argumenta: broj misionara i broj kanibala!");
                    }
                    return;
                }
                M = Int16.Parse(args[0]);
                N = Int16.Parse(args[1]);
                if (comm.Size != M + N + 1)
                {
                    if (processId == 0)
                    {
                        Console.WriteLine("Broj procesa je razlicit od broja kanibala, misionara i camca zajedno.");
                    }
                    return;
                }
                if (processId == 0)
                {
                    BoatProcess(comm);
                }
                else if (processId >= 1 && processId <= M)
                {
                    Process(comm, false);
                }
                else
                {
                    Process(comm, true);
                }
            }
        }


        public static void BoatProcess(Intracommunicator comm)
        {
            string myStringID = StringIdentityOFProcess(processId) + ": ";
            Badge badge = new Badge();
            badge.source = processId;
            for (int i = 0; i <= M + N; i++)
            {
                badge.ring.Add(i);
            }
            Stopwatch timer = new Stopwatch();
            timer.Start();

            while (true)
            {
                Console.WriteLine("Čamac: Čekam na ukrcaj!");
                timer.Reset();
                timer.Start();
                int destination = badge.GetNeighProcessId(processId);
                if (destination == processId)
                {
                    System.Threading.Thread.Sleep((int)LOAD_TIME / 2);
                    Console.WriteLine(myStringID + "Nema nikog u čamcu. Završavam s radom.");
                    break;
                }
                Badge badgeRcv = badge;
                while (true)
                {
                    badgeRcv.source = processId;
                    Console.WriteLine(myStringID + "Šaljem značku procesu " + StringIdentityOFProcess(destination));
                    comm.Send<Badge>(badgeRcv, destination, 0);
                    Badge currBadge = comm.Receive<Badge>(MPI.Unsafe.MPI_ANY_SOURCE, 0);
                    Console.WriteLine(myStringID + "Primio značku od procesa " + StringIdentityOFProcess(currBadge.source));
                    badgeRcv = currBadge;
                    if (timer.ElapsedMilliseconds > LOAD_TIME)
                    {
                        break;
                    }
                    else if (currBadge.IsBoatFull())
                    {
                        System.Threading.Thread.Sleep((int)(LOAD_TIME - timer.ElapsedMilliseconds + 100));
                        break;
                    }
                }
                if (badgeRcv.IsBoatEmpty())
                {
                    badge.RED_PILL = true;
                    if (destination != processId)
                    {
                        comm.Send<Badge>(badge, destination, 0);
                    }
                    Console.WriteLine(myStringID + "Nema nikog u čamcu. Završavam s radom.");
                    break;
                }
                string print = myStringID + "Prevozim sljedeće osobe: ";
                Badge redPillBadge = new Badge();
                redPillBadge.RED_PILL = true;
                foreach (var entry in badgeRcv.passengers)
                {
                    print += StringIdentityOFProcess(entry) + ",";
                    comm.Send<Badge>(redPillBadge, entry, 0);
                }
                print = print.Substring(0, print.Length - 1);
                Console.WriteLine(print);
                Console.WriteLine();
                badgeRcv.UnloadBoat();
                badge = badgeRcv;
                System.Threading.Thread.Sleep(200);

            }
        }

        public static void Process(Intracommunicator comm, bool isCannibal)
        {
            string myStringID = StringIdentityOFProcess(processId) + ": ";
            Random random = new Random();
            int waitingTime = random.Next(1000 * 10 + processId * 500);//koliko ćemo cekati tj. kad će biti spreman za ukrcaj
            Stopwatch timer = new Stopwatch();
            timer.Start();
            bool isInside = false;
            while (true)
            {
                Badge currBadge = comm.Receive<Badge>(MPI.Unsafe.MPI_ANY_SOURCE, 0);
                if (currBadge.RED_PILL)
                {
                    break;
                }
                Console.WriteLine(myStringID + "Primio značku od procesa " + StringIdentityOFProcess(currBadge.source));
                System.Threading.Thread.Sleep(500);
                currBadge.source = processId;
                if (isInside)
                {
                    Console.WriteLine(myStringID + "Već sam u čamcu! Šaljem značku procesu: "
                        + StringIdentityOFProcess(currBadge.GetNeighProcessId(processId)));
                    comm.Send<Badge>(currBadge, currBadge.GetNeighProcessId(processId), 0);
                }
                else if (timer.ElapsedMilliseconds < waitingTime)
                {
                    Console.WriteLine(myStringID + "Ne želim još uci u čamac, šaljem značku procesu: "
                        + StringIdentityOFProcess(currBadge.GetNeighProcessId(processId)));
                    comm.Send<Badge>(currBadge, currBadge.GetNeighProcessId(processId), 0);
                }
                else if (!currBadge.CanEntry(isCannibal))
                {
                    Console.WriteLine(myStringID + "Ne mogu ući u čamac, šaljem značku procesu: "
                        + StringIdentityOFProcess(currBadge.GetNeighProcessId(processId)));
                    comm.Send<Badge>(currBadge, currBadge.GetNeighProcessId(processId), 0);
                }
                else
                {
                    currBadge.GetInBoat(isCannibal, processId);
                    Console.WriteLine(myStringID + "Ulazim u čamac!");
                    isInside = true;
                    comm.Send<Badge>(currBadge, currBadge.GetNeighProcessId(processId), 0);

                }
            }
            timer.Stop();

        }


        public static string StringIdentityOFProcess(int processID)
        {
            if (processID == 0)
            {
                return "Čamac";
            }
            else if (processID >= 1 && processID <= M)
            {
                return "Misionar " + processID;
            }
            else
            {
                return "Kanibal " + (processID - M);
            }
        }

    }
}


