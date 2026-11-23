from solution import solution
tests = [
# žádná dvojice nemá společnou cifru => lze vybrat libovolné jedno číslo
([99, 88, 77], 1),
# společná cifra je "1"
([10, 11, 12, 91], 4),
# validní volba: 50, 15, 51, 10, 15
([50, 30, 15, 51, 10, 20, 15], 5),
]

for (numbers, expected) in tests:
    assert solution(numbers) == expected