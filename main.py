import asyncio
from scrapper import run_playwright


async def main():
    # PREPARED FOR PARALLEL BROWSERS OPENED

    # number_of_task = 1
    # number_of_page = 51
    # pages = [
    #     1
    # ]

    # tasks = []
    # for pg in pages:
    #     tasks.append(run_playwright(pg))

    tasks = []
    tasks.append(run_playwright(page_start=1,page_end=1)) # only scrap products in page 1

    # add other tasks
    # tasks.append(run_playwright(page_start=2,page_end=2)) # only scrap products in page 2
    # tasks.append(run_playwright(page_start=3,page_end=5))
    # tasks.append(run_playwright(page_start=6,page_end=10))


    await asyncio.gather(*tasks)

# Run the main function
asyncio.run(main())