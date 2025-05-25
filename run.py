from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use 'spawn' on platforms like Windows; 'fork' is okay on UNIX.
    if os.name != 'nt':
        multiprocessing.set_start_method("fork", force=True)

    sem = multiprocessing.Semaphore(1)
    process = multiprocessing.Process(target=worker, args=(sem,))
    process.start()
    process.join()

    app.run(debug=True)

