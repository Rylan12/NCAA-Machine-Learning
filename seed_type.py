from enum import Enum


class SeedType(Enum):
    OneSixteen = {'1', '16'}
    TwoFifteen = {'2', '15'}
    ThreeFourteen = {'3', '14'}
    FourThirteen = {'4', '13'}
    FiveTwelve = {'5', '12'}
    SixEleven = {'6', '11'}
    SevenTen = {'7', '10'}
    EightNine = {'8', '9'}

    @classmethod
    def get_type_index(cls, name):
        if name == 'OneSixteen':
            return 1
        if name == 'TwoFifteen':
            return 2
        if name == 'ThreeFourteen':
            return 3
        if name == 'FourThirteen':
            return 4
        if name == 'FiveTwelve':
            return 5
        if name == 'SixEleven':
            return 6
        if name == 'SevenTen':
            return 7
        if name == 'EightNine':
            return 8

    def __gt__(self, other):
        return min(self.value) > min(other.value)

    def __lt__(self, other):
        return min(self.value) < min(other.value)
