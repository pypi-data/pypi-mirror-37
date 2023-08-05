# Han2Jamo 

한글 to 자모로 바꿔주는 가장 빠르고 편리한 라이브러리

[![CircleCI](https://circleci.com/gh/codertimo/han2jamo.svg?style=shield)](https://circleci.com/gh/kor2vec/kor2vec)
[![LICENSE](https://img.shields.io/github/license/codertimo/han2jamo.svg)](https://github.com/kor2vec/kor2vec/blob/master/LICENSE)
[![PyPI - Status](https://img.shields.io/pypi/status/han2jamo.svg)]()
[![PyPI](https://img.shields.io/pypi/v/han2jamo.svg)]()
[![GitHub stars](https://img.shields.io/github/stars/codertimo/han2jamo.svg)](https://github.com/kor2vec/kor2vec/stargazers)




## Installation

```
pip install han2jamo
```

## Usage

```python3
hand2jamo = Han2Jamo()

# 한글문장 -> 자모 : str
han2jamo.str_to_jamo("안녕 내 이름은 뽀로로야")
>> "ㅇㅏㄴㄴㅕㅇ ㄴㅐ ㅇㅣㄹㅡㅁㅇㅡㄴ ㅃㅗㄹㅗㄹㅗㅇㅑ"

# 자모 -> 한글문장 복원
hand2jamo.jamo_to_str("ㅇㅏㄴㄴㅕㅇ ㄴㅐ ㅇㅣㄹㅡㅁㅇㅡㄴ ㅃㅗㄹㅗㄹㅗㅇㅑ")
>> "안녕 내 이름은 뽀로로야"

# 한글 한글자 -> 자모
hand2jamo.char_to_jamo("꾹")
>> ("ㄲ", "ㅜ", "ㄱ")

## 자모 -> 한글 한글자 복원
hand2jamo.jamo_to_char("ㄲㅜㄱ")
>> "꾹"

```

