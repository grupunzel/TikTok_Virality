<h1>TikTok_Virality</h1>
This project goal was to make an interactive web interface for researching the TikTok viralty based on the number of streams the song receives per day. The project was implemented using Streamlit.

<h2>Documentation</h2>
In this project I used the libraries <a href='https://docs.streamlit.io/'>streamlit</a> and <a href='https://pandas.pydata.org/docs/'>pandas</a>.

<h2>How to use</h2>
On the main page of the project you can view a linear graph of the dependency and a filtered table.
On the side bar you can choose filters like genres of the popular songs, their realese years, daily streams, etc.
Over the graph there is an information about the aount of all streams, their average, the most popular artist, average numbers of weeks on charts, peak positions and song sentiments.
To download the filtered file press the 'Download as CSV' if you want a csv file and 'Download as xlsx' if you need an Excel file.

<h2>Instructions</h2>
To test the project use these instructions:<br><br>
1. Create a directory on your computer and copy there two files: 'main.py' and 'music_dataset.csv'.<br><br>
2. Open the Command Prompt, go to the directory with the project and install a virtual environment by running this code:<br><br>
<pre>python -m venv env</pre><br>
3. Activate your virtual evironment. Go to the repository 'env', then 'Scripts' and run 'activate'.<br><br>
4. Install the libraries 'pandas' and 'streamlit':<br><br>
<pre>pip install pandas</pre><br>
<pre>pip install streamlit</pre><br>
5. To view the project run the code below:<br><br>
<pre>streamlit run main.py</pre><br>
Now you ccan use this project.

<h2>Attached files</h2>
<ul>
  <li><b>main.py</b> - file with the script</li>
  <li><b>music_dataset.csv</b> - csv file with the dataset</li>
  <li><b>requirments.txt</b></li>
</ul>
