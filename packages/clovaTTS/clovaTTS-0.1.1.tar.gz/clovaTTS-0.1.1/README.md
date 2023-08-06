# clovaTTS

clova-tts performs text-to-speech using [Naver Clova Speech Synthesis API](https://developers.naver.com/products/clova/tts/).

## Installation

  ```
  pip install clovaTTS
  ```

## Quickstart
  ```
  from clovaTTS import clovaTTS
  
  tts = clovaTTS("mijin", "<client_id>", "<client_secret>")

  # Input text (in Korean)
  text = "그래요. 많은 분들이 저를 찾고 있지요."

  # Perform Text-to-Speech
  speech = tts.tts(text)

  # Save the output into a file
  tts.save("output.mp3", speech)
  ```

## Contact
Any questions or assistance? Please contact me at minsu(at)etri.re.kr.
