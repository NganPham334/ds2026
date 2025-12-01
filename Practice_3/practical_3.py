from mpi4py import MPI
import sys
import os


def run():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Rank 0: Sender
    if rank == 0:
        if len(sys.argv) < 2:
            print("Usage: mpiexec -n 2 python mpi_transfer.py <filename>")
            sys.exit(1)

        filepath = sys.argv[1]
        filename = os.path.basename(filepath)

        # Send filename
        comm.send(filename, dest=1, tag=0)

        # Send content chunks
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                comm.send(chunk, dest=1, tag=1)

        # Send EOF
        comm.send(None, dest=1, tag=1)
        print("Sender: Finished.")

    # Rank 1: Receiver
    elif rank == 1:
        # Receive filename
        filename = comm.recv(source=0, tag=0)
        print(f"Receiver: Saving to 'recv_{filename}'")

        with open(f"recv_{filename}", 'wb') as f:
            while True:
                chunk = comm.recv(source=0, tag=1)
                if chunk is None:
                    break
                f.write(chunk)

        print("Receiver: Finished.")


if __name__ == "__main__":
    run()