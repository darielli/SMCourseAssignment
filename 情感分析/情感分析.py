from cnsenti import Emotion
from cnsenti import Sentiment
import pandas as pd
def emotion(str):
    emotion = Emotion()
    test_text = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
    result = emotion.emotion_count(str)
    return result

def sentiment(str):
    senti = Sentiment()  # 两txt均为utf-8编码
    test_text = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
    result1 = senti.sentiment_count(test_text)
    result2 = senti.sentiment_calculate(str)
##    print('sentiment_count', result1)
##    print('sentiment_calculate', result2)
    return result2