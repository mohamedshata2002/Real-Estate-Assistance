
print("Inializing..... \n")
from Assistance import sql_transfromer,choser,real_state_assistance,sql_excuter,arabic_transformer
from sound import record_audio,save_audio,encoder
from mail import mail
from bidi.algorithm import get_display
from  elevenlabs import play
from elevenlabs.client import ElevenLabs
from apis import voice
import arabic_reshaper


button =None
breaker = 0
client = ElevenLabs(api_key = voice)
while True :
    if button == None:
        button = input("Your name please \n")
    
    print("...start recording \n")
    audio_data = record_audio()
    save_audio("./output/output.wav", audio_data)
    query = encoder("./output/output.wav")
    
    query=arabic_transformer.invoke(query)
    data = sql_transfromer.invoke(query)
    reshaped_text = arabic_reshaper.reshape(query)
    bidi_text = get_display(reshaped_text)
    print(bidi_text)
    dataset = sql_excuter(data['sql'])
    print(dataset)
    if dataset.empty  ==False:
        
        result = real_state_assistance.invoke(dataset)
        audio = client.generate(text=result,voice="Rachel",  model="eleven_multilingual_v2")
        play(audio)
        reshaped_text = arabic_reshaper.reshape(result)
        bidi_text = get_display(reshaped_text)
        print(bidi_text)
        print("...start recording \n")
        audio_data = record_audio()
        
        save_audio("./output/output.wav", audio_data)
        query = encoder("./output/output.wav")
        query=arabic_transformer.invoke({"words":query})
        print(query)
        chosen = choser.invoke({"context":dataset.to_string(),"inst":query})
        
        print(chosen)
        mail(button,chosen)
        break
    else:
        result="لا يوجد بيت مطابق للموصفات"
        audio = client.generate(text=result,voice="Rachel",  model="eleven_multilingual_v2")
        play(audio)
       
    breaker =+1
    if breaker==10:
        break
        