![[Screenshot 2024-10-11 at 18.12.51.png]]
## Encoder
Здесь есть N слоев. Каждый слой состоит из 2х подслоев с последующей их нормализацией. Выход каждого слоя: LayerNorm(x + Sublayer(x)).
1 подслой: multi-head self-attention
2 подслой: positionwise fully connected feed-forward network
## Decoder
Добавляется 