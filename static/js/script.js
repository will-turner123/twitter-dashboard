window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

function doBarChart(data, broker){
    var barChartElement = document.getElementById('tweet-volume').getContext('2d');
    var lineChartOptions = {
        type: 'bar',
        // data: JSON.parse(data),
        data: {
            labels: data.tweet_volume.x,
            datasets: [{
                label: "Sentiment Over Time",
                backgroundColor: window.chartColors.blue,
                borderColor: window.chartColors.blue,
                fill: false,
                data: data.tweet_volume.y,
                yAxisID: 'y-axis-1'
            }] 
        },
        options: {
            responsive: true,
            hoverMode: 'index',
            stacked: false,
            title: {
                display: false,
                text: "Tweet Volume Over Time"
            },
            scales: {
                x: {
                    type: 'timeseries'
                },
                yAxes: [{
                    type: 'linear',
                    display: true,
                    position: 'left',
                    id: 'y-axis-1'
                }]
            }
        }
    }
    barChart = new Chart(barChartElement, lineChartOptions);
}
  

function doLineChart(data, broker){
    var sentimentOverTime = document.getElementById('sentiment-line').getContext('2d');
    var lineChartOptions = {
        type: 'line',
        // data: JSON.parse(data),
        data: {
            labels: data.sentiment_over_time.x,
            datasets: [{
                label: "Sentiment Over Time",
                backgroundColor: window.chartColors.red,
                borderColor: window.chartColors.red,
                fill: false,
                data: data.sentiment_over_time.y,
                yAxisID: 'y-axis-1'
            }] 
        },
        options: {
            responsive: true,
            hoverMode: 'index',
            stacked: false,
            title: {
                display: false,
                text: "Sentiment Over Time"
            },
            scales: {
                x: {
                    type: 'timeseries'
                },
                yAxes: [{
                    type: 'linear',
                    display: true,
                    position: 'left',
                    id: 'y-axis-1'
                }]
            }
        }
    }
    lineChart = new Chart(sentimentOverTime, lineChartOptions);
}

/* <li class="list-group-item">
<!-- display sentiment -->
<p class="text-success" style="float:right;"><i class="far fa-smile"></i> 0.32</p>
<blockquote class="blockquote text-center">
   <p class="mb-0">Example tweet lorem ipsum dolor sit amet</p>
   <footer class="blockquote-footer">Twitter User</footer>
</blockquote>
</li> */
function writePositiveTweets(data){
    $('#positiveTweets').empty();
    var i;
    var positive_user = data.best_10.username;
    var positive_tweet = data.best_10.tweet;
    var positive_sentiment = data.best_10.sentiment;
    for(i=0; i < positive_tweet.length; i++){
        // worst way of doing this ever lol
        var html_string = "<li class='list-group-item'><p class='text-success' style='float: right;'><i class='far fa-smile'></i>"
        html_string = html_string + positive_sentiment[i] + "</p><blockquote class='blockquote text-center'><p class='mb-0'>" + positive_tweet[i]
        html_string = html_string + "</p>" + "<footer class='blockquote-footer'>" + positive_user[i] + "</footer></blockquote></li>"
        console.log(html_string);
        $('#positiveTweets').append(html_string);
    }
}
function writeNegativeTweets(data){
    $('#negativeTweets').empty();
    var i;
    var positive_user = data.worst_10.username;
    var positive_tweet = data.worst_10.tweet;
    var positive_sentiment = data.worst_10.sentiment;
    for(i=0; i < positive_tweet.length; i++){
        // worst way of doing this ever lol
        var html_string = "<li class='list-group-item'><p class='text-danger' style='float: right;'><i class='far fa-frown'></i>"
        html_string = html_string + positive_sentiment[i] + "</p><blockquote class='blockquote text-center'><p class='mb-0'>" + positive_tweet[i]
        html_string = html_string + "</p>" + "<footer class='blockquote-footer'>" + positive_user[i] + "</footer></blockquote></li>"
        console.log(html_string);
        $('#negativeTweets').append(html_string);
    }
}


function getData(broker="RobinhoodApp"){
    url = "/data?broker=" + broker
    fetch(url).then(function (response) {
        return response.json();
    }).then(function (text) {
        doLineChart(text, broker);
        doBarChart(text, broker);
        document.getElementById('brokerName').innerHTML = broker
        // update active tab
        
        // update best & worst tweets
        document.getElementById('bestTweet').innerHTML = text.best.tweet;
        document.getElementById('bestUser').innerHTML = text.best.user;
        document.getElementById('worstTweet').innerHTML = text.worst.tweet;
        document.getElementById('worstUser').innerHTML = text.worst.user;
        // overall sentiment
        document.getElementById('overall_sentiment').innerHTML = text.overall_sentiment;
        // write 10 most recent positive & negative tweets
        writePositiveTweets(text);
        writeNegativeTweets(text);
        // update ranking at top of page
        document.getElementById('rank1').innerHTML = text['ranks']['1']['name'];
        document.getElementById('rank2').innerHTML = text['ranks']['2']['name'];
        document.getElementById('rank3').innerHTML = text['ranks']['3']['name'];
        document.getElementById('rank4').innerHTML = text['ranks']['4']['name'];
        document.getElementById('rank5').innerHTML = text['ranks']['5']['name'];
    });
}

window.onload = function(){
    
    var myData = getData();
    console.log('myData:')
    console.log(myData);
}
