var StartTime = new Date().getTime(); //here you're making new Date object
var counter = document.getElementById("counter")
var finish = document.getElementById("finish")
let TopList = document.getElementById('TopList')
let message = document.getElementById('message')
let toplist = document.getElementsByName('toplist')

function TopListShow() {
  TopList.style.display = "block";
  // TopList.style.paddingRight = "17px";
  TopList.className="modal fade show"; 
}
function ToListHide() {
  TopList.style.display = "none";
  TopList.className="modal fade";
}

document.getElementById('Close1').addEventListener('click', ToListHide)
document.getElementById('Close2').addEventListener('click', ToListHide)

function convertTime(timeLeft, withDays) {
  var days = Math.floor(timeLeft / (1000 * 60 * 60 * 24)); //conversion miliseconds on days 
  if (days < 10) days="0"+days; //if number of days is below 10, programm is writing "0" before 9, that's why you see "09" instead of "9"
  var hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)); //conversion miliseconds on hours
  if (hours < 10) hours="0"+hours;
  var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60)); //conversion miliseconds on minutes 
  if (minutes < 10) minutes="0"+minutes;
  var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);//conversion miliseconds on seconds
  if (seconds < 10) seconds="0"+seconds;
  var result = hours + "h " + minutes + "m " + seconds + "s"
  if (withDays) {
    result = days + "d " +result
  } 
  return result
}

function updateTopList(data) {
  for (var i=0;i<Math.min(10, 1 * data['records']);i++) {
          console.log('toplist',data['top'][i])
          toplist[i].classList.remove("d-none")
          toplist[i].children[0].innerText = data['top'][i][0]
          toplist[i].children[1].innerText = data['top'][i][1]
          toplist[i].children[2].innerText = data['top'][i][2]
          toplist[i].children[3].innerText = data['top'][i][3]
        }
}

function detailTime(timeLeft) {
  var result = {}
  result['days']  = Math.floor(timeLeft / (1000 * 60 * 60 * 24)); //conversion miliseconds on days 
  result['hours']  = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)); //conversion miliseconds on hours
  result['minutes']  = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60)); //conversion miliseconds on minutes 
  result['seconds']  = Math.floor((timeLeft % (1000 * 60)) / 1000);//conversion miliseconds on seconds
  return result
}
function getTempURL(url, timeLeft) {
  let temp = url +
  document.getElementById('gameType').innerText + '-' + 
  document.getElementById('method').innerText + '-' + 
  document.getElementById('level').innerText+ '/' + 
  document.getElementById('game_id').innerText+ '/'
  if (document.getElementById('result')) {
    temp += document.getElementById('result').innerText.replace("%","")+ '/'
  }
  else {
    temp += 100 + '/'
  }
  var detal_time = detailTime(timeLeft)
  temp += detal_time['hours'] + '/' +detal_time['minutes'] + '/'+detal_time['seconds'] + '/'
  return temp
}

function fetchTolList(timeLeft) {
  var temp_url = getTempURL('/scoring/score_check/', timeLeft)
  console.log('fetch start.', temp_url)
  fetch(temp_url)
    .then(response=> response.json())
      .then(data => {
        message.innerHTML = data['message']
        updateTopList(data)
        if (data['status'] == 'success') {
          TopListShow();
          document.getElementById('saveBTN').addEventListener('click', function(event) {
            console.log(event.target.innerText)
            if (event.target.innerText == "Zamknij") {
              ToListHide();
              return;
            }
            else {
              event.target.innerText = "Zamknij";
            }
            console.log(event.target.innerText)
            temp_url = getTempURL('/scoring/score_update/', timeLeft)
            console.log('fetch start.', temp_url)
            fetch(temp_url)
            .then(response2 => response2.json())
              .then(data2 => {
                console.log(data2)
                message.innerHTML = data2['status'] + "<br>" + data2['message']
                updateTopList(data2)
                document.getElementById('Close2').style.display = "none";
              })
          })
        }
      })
}

var timing = setInterval( // you're making an interval - a thing, that is updating content after number of miliseconds, that you're writing after comma as second parameter
  function () {
    var currentTime = new Date().getTime(); //same thing as above
    var timeLeft = currentTime - StartTime; //difference between time you set and now in miliseconds
    var days = Math.floor(timeLeft / (1000 * 60 * 60 * 24)); //conversion miliseconds on days 
    if (days < 10) days="0"+days; //if number of days is below 10, programm is writing "0" before 9, that's why you see "09" instead of "9"
    var hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)); //conversion miliseconds on hours
    if (hours < 10) hours="0"+hours;
    var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60)); //conversion miliseconds on minutes 
    if (minutes < 10) minutes="0"+minutes;
    var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);//conversion miliseconds on seconds
    if (seconds < 10) seconds="0"+seconds;

    counter.innerHTML =  hours + "h " + minutes + "m " + seconds + "s"; // putting number of days, hours, minutes and seconds in div, 
    counter.value = timeLeft;
    //which id is countdown
    if (+finish.innerText > 0) {
      var currentTime = new Date().getTime();
      var timeLeft = currentTime - StartTime;
      document.getElementById('finalTime').innerText =  timeLeft
      clearInterval(timing);
      result = ''
      if (document.getElementById('result')) {
        result = ". Twój wynik quizu wynosi " +document.getElementById('result').innerText
      }
      counter.innerHTML = "Brawo!  " + convertTime(timeLeft, false) + result; 
      if (document.getElementById('end_site')) {
        document.getElementById('end_site').classList.remove("d-none");
        document.getElementById('end_site').innerHTML = "Brawo!  " + convertTime(timeLeft, false) + result; 
      }
      fetchTolList(timeLeft)
    }
  }, 1000);
