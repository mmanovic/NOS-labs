using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NOS_lab1
{
    [Serializable]
    class Badge
    {
        public int nOfMissionary = 0;
        public int nOfCannibal = 0;
        public List<int> ring = new List<int>();
        public List<int> passengers = new List<int>();
        public bool RED_PILL = false;
        public int source;
        public Badge()
        {

        }

        public int GetNeighProcessId(int myId)
        {
            return ring[(ring.IndexOf(myId) + 1) % ring.Count];
        }

        public bool CanEntry(bool isCannibal)
        {
            if (isCannibal)
            {
                if ((nOfCannibal == 1 && nOfMissionary == 1) || (nOfMissionary + nOfCannibal == 3))
                {
                    return false;
                }
                return true;
            }
            else
            {
                if ((nOfCannibal == 2) || (nOfMissionary + nOfCannibal == 3))
                {
                    return false;
                }
                return true;
            }
        }

        public void GetInBoat(bool isCannibal, int IdOfPassenger)
        {
            if (isCannibal)
            {
                nOfCannibal++;
            }
            else
            {
                nOfMissionary++;
            }
            passengers.Add(IdOfPassenger);
        }

        public bool IsBoatFull()
        {
            return nOfMissionary + nOfCannibal >= 3;
        }

        public bool IsBoatEmpty()
        {
            return nOfCannibal + nOfMissionary == 0;
        }

        public void UnloadBoat()
        {
            foreach (var entry in passengers)
            {
                ring.Remove(entry);
            }
            passengers.Clear();
            nOfMissionary = 0;
            nOfCannibal = 0;
        }
    }
}
