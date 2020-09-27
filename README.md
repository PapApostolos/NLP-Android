# NLP-Android App

This Application concerns the development of an Android interface, which in sync with a python server, is able able to categorize natural text in different classes. 
For categorization are used [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory)  and [GRU](https://en.wikipedia.org/wiki/Gated_recurrent_unit) rnn models.<br>
> The project consist of:
> * A [client–server model](https://en.wikipedia.org/wiki/Client%E2%80%93server_model) (android interface/python sever).
> * and the Recurrent Neural Networks ([RNNs](https://en.wikipedia.org/wiki/Recurrent_neural_network)) sequential models.
>
> The above work is part of the final project for the MSc course in deep neural networks ([DSIT](http://dsit.di.uoa.gr/)).

***
## **Client–Server model**

The user uses the app to pass the text data to the device and sends the input to the server throw a socket channel. <br> After, the server has to reify two separate tasks:

1. Detect the most significant sentences on the text based on the [Term frequency](https://www.opinosis-analytics.com/knowledge-base/term-frequency-explained/#.X3DU7u1S_BV) scores. 
2. Runs a rnn model to classify the input text to business, medicine, science or entertainment category.

Subsequently, The server sends a response to the client, and the connection is terminated. The final output is displayed to the user. 

 
 <table  >
   <tr >
    <th>Prompt Message</th>
    <th>Reply</th>
  </tr>
  <tr >
    <td><img src="photos/UserInterface.jpg" width="215" height="420" /></td>
    <td><img src="photos/ui_SpOdyssey.jpg"width="215" height="420"/></td>
  </tr>

</table> 

***
## **RNN models**
The performace of the LSTM and GRU models is presented on the following diagrams:
