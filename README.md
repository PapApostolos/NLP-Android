# NLP-Android App

This Application concerns the development of an Android interface, which in sync with a python server, is able able to categorize natural text in different classes. 
For categorization are used [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory)  and [GRU](https://en.wikipedia.org/wiki/Gated_recurrent_unit) rnn models.<br>
> The project consist of:
> * A [client–server model](https://en.wikipedia.org/wiki/Client%E2%80%93server_model) (android interface/python sever).
> * and the Recurrent Neural Networks ([RNNs](https://en.wikipedia.org/wiki/Recurrent_neural_network)) sequential models.
>
> The above work is part of the final project for the MSc course in deep neural networks ([DSIT](http://dsit.di.uoa.gr/)).

***
<h1>Client–Server model</pre></h1>

The user opens a mobile device and passes the input on the prompt frame. Then the server receives the data from the app throw a socket channel and reifies two separate tasks:
1. Runs a rnn model so as to classify the input text to business, medicine/health, science/technology or entertainment category.
2. Detect the most significant sentences on the text based on the Term frequency scores. 

Subsequently, sends a response to the client, and the connection is terminated. The reply is displayed to the user. 


 *<h2>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Android Interface</h2>*
 


 
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
