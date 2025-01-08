def my_decorator(func):
    def wrapper():
        print(f"Running {func.__name__}")
        func()
        print("Completed.")
    return wrapper

@my_decorator
def do_this():
    print("Doing this.")

@my_decorator
def do_that():
    print("Doing that.")

# do_this()
# do_that()

def add_numbers(*args):
    total = 0
    for num in args:
        total+=num

    print("Sum is:", total)

add_numbers(1,2,3,4,5,6,7,8,9,10)