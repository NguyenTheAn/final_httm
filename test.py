from google_trans_new import google_translator  
translator = google_translator()  
text= 'mặt hàng này rất tệ, không đúng với giá thành'
translate_text = translator.translate(text, lang_tgt='en')  
print(translate_text)