from collections import deque


nums = [str(i) for i in range(10)]
chars_low = [chr(ord('a')+i) for i in range(26)]
chars_up = [chr(ord('A')+i) for i in range(26)]
chars_all = chars_low + chars_up


def brute_force_generator(chars, condition, max_len = 8):
    queue = deque([''])
    while queue:
        string = queue.popleft()
        if len(string) > max_len:
            return
        if condition(string):
            yield string
        for char in chars:
            if len(string) <= max_len:
                queue.append(string + char)
    return

def num_bf(min_len = 4, max_len = 8):
    chars = nums
    def condition(s):
        return min_len <= len(s) <= max_len

    yield from brute_force_generator(chars, condition, max_len)

def char_bf(min_len, max_len = 8):
    chars = chars_all + nums
    def condition(s):
        return min_len <= len(s) <= max_len and s[0] in chars_all

    yield from brute_force_generator(chars, condition, max_len)


def main():
    # for i in num_bf(4,4):
    #     print(i)
    for i in char_bf(4,4):
        print(i)

if __name__ == '__main__':
    main()
