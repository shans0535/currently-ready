from typing import Dict
import functools
import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List
import time


def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter = counter + 1
        time.sleep(1)
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 3, 5, 6, 7]
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []
        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))
        results = await asyncio.gather(*call_coros)
        for result in results:
            print(result)


def map_frequency(text: str) -> Dict[str, int]:
    words = text.split(' ')
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] = frequencies[word] + 1
        else:
            frequencies[word] = 1
    return frequencies


def merge_dictionaries(first: Dict[str, int],
                       second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    print(f'first : {first}\nsecond: {second}')
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


# lines = ["I know what I know",
#          "I know that I know",
#          "I don't know much",
#          "They don't know much"]

# mapped_results = [map_frequency(line) for line in lines]

# for result in mapped_results:
#     print(result)

# print(functools.reduce(merge_dictionaries, mapped_results))


if __name__ == "__main__":
    asyncio.run(main())
