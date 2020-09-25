package waseemkntar.connectwithpython;

import android.content.Context;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Html;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class MainActivity extends AppCompatActivity {

    Button connectPythonBut;
    static TextView replyMessageTextView;
    EditText data2SendEditText;
    static final String SERVER_IP = "192.168.1.3"; // The SERVER_IP must be the same in server and client
    static final int PORT = 8080; // You can put any arbitrary PORT value

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connectPythonBut = (Button) findViewById(R.id.connectPythonBut);
        replyMessageTextView = (TextView) findViewById(R.id.replyMessageTextView);
        replyMessageTextView.setVisibility(View.INVISIBLE);


        data2SendEditText = (EditText) findViewById(R.id.data2SendEditText);
        String text="<span style='color:gray;'> <i> Import <u>text</u> or  <u>link</u></i>  </span>" ;
        data2SendEditText.setHint(Html.fromHtml(text, Html.FROM_HTML_MODE_COMPACT));
        data2SendEditText.setGravity(Gravity.CENTER);


        connectPythonBut.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View view) {

                String text= data2SendEditText.getText().toString();
                String Newtext="<span style='color:gray;text-wrap: balance;'> "+text+"  </span>" ;
                data2SendEditText.setHint(Html.fromHtml(text, Html.FROM_HTML_MODE_COMPACT));
                data2SendEditText.setGravity(Gravity.NO_GRAVITY);


                replyMessageTextView.setVisibility(View.VISIBLE);
                replyMessageTextView.setText("Waiting python reply");

                ConnectPyTask task = new ConnectPyTask();
                ConnectPyTask.context = getApplicationContext();
                task.execute(data2SendEditText.getText().toString());
            }
        });
    }
    static class ConnectPyTask extends AsyncTask<String, Void, String>
    {
        static Context context = null;
        static float startTime = 0, endTime = 0;
        @Override
        protected String doInBackground(String... data) {
            try {
                startTime = System.currentTimeMillis();
                Socket socket = new Socket(SERVER_IP, PORT); //Server IP and PORT
                Scanner sc = new Scanner(socket.getInputStream());
                PrintWriter printWriter = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
                printWriter.write(data[0]); // Send Data
                printWriter.flush();



                replyMessageTextView.setGravity(Gravity.NO_GRAVITY);
                replyMessageTextView.setMovementMethod(new ScrollingMovementMethod() );


                String result="<span> <b  style='color:black;'> Categ:</b> <i> "+sc.nextLine()+" "+sc.nextLine()+"</i> <br><br> </span>" +"<span> <b  style='color:black;'> Summary:</b> <i> "+sc.nextLine()+"</i> </span>" ;
                replyMessageTextView.setText(Html.fromHtml(result, Html.FROM_HTML_MODE_COMPACT));

                /**
                result="<span> <b  style='color:black;'> Categ:</b> <i> "+sc.nextLine()+" "+sc.nextLine()+"</i> <br><br> </span>" ;

                result=result+"<b  style='color:black;'> Summary: </b>" ;


                while(sc.hasNextLine() ){
                  result=result +" "+ sc.nextLine();
                }

                 */

                System.out.println(result);



                //replyMessageTextView.setText(result);
                replyMessageTextView.setText(Html.fromHtml(result, Html.FROM_HTML_MODE_COMPACT));



            }catch (Exception e){
                Log.d("Exception", e.toString());
            }
            return null;
        }

        @Override
        protected void onPostExecute(String s) {
            endTime = System.currentTimeMillis();
            String execTime = String.valueOf((endTime - startTime)/1000.0f);
            Toast.makeText(context, "Time execution is: " + execTime + "s", Toast.LENGTH_SHORT).show();
        }
    }
}
