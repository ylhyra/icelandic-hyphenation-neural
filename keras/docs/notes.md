* window: 24
* hidden_layers: 100
* epochs: 12
* loss: 0.0427
* accuracy: 0.9841

---



Post-training quantization
https://www.tensorflow.org/lite/performance/post_training_quantization


2020-10-26
reyni að gera bara eitt continuous output

2020-10-27
dýpt gerir ekkert betra


# Tilraunir

* 50->25 dropout 0.3 gefur minnst rsme 0.30
* 50->25 dropout 0 gefur minnst rsme 0.25
* 100->100->100 dropout 0 gefur minnst rsme 0.25
* 150->150->100->100 dropout 0 gefur minnst rsme 0.23
* 400->250->100->100 dropout 0 gefur minnst rsme 0.21
* 500->400->200->100 dropout 0 gefur minnst rsme 0.21, 0.19 með smá lærdómi á minni
  * 0.16 kl 20:14, heiti best_model_500_mjög gott nr 3
  * 0.12 kl 20:14, heiti best_model_500_mjög gott nr 4
