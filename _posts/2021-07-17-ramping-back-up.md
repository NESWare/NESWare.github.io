---
layout: post
title: "Ramping Back Up"
subtitle: "Do you want to continue? [Y/n]"
author: Lnk2past
tags: storytime
readtime: 5
---

I am finally getting back to coding outside of work. <!--more--> I certainly have not stopped coding all this time, I have just been spending my time at home doing anything and everything else.

## What is New?

In my last post I detailed just how burned out by coding I felt - these last several months mostly avoiding it at home was much needed. I have dabbled a bit here and there after work on a few things over the past few weeks and find myself wanting to do more and more each day.

Back in October I started a new job working in Python doing systems analysis. While I hardly do any actual systems analysis, I have had great freedoms with the tooling and improvements I have been bringing to the department. The department I work for is largely struggling to use modern tools, libraries, and processes. Much of what the other analysts use are very old and horribly architected processes and scripts (an odd amalgam of old MATLAB, Python, and Bash). Nothing makes sense, but things work just enough to get by. Getting by is not good enough though - things there really need to be better.

While the current state is terribly frustrating, it has given me an opportunity to educate others and introduce them to new technologies and methods that they would not otherwise learn for some time. I have primarily been focused on automating manual tasks, but I have also been spending a lot of time in recent months developing dashboards and visualizations for our analysis stakeholders (i.e. interactive and shareable analysis).

While working these projects I have been relying very heavily on producing browser-based content. I have been learning a good amount of HTML/CSS/JavaScript, and I have been enjoying it far more than I thought I would. It is indeed different and annoying at times, but I have a much better understanding of how these technologies work now.

## What is Next?

From here, I need to prepare for the Fall 2021 semester. I am teaching a new Data Visualization course, and this means writing new course material from scratch - this is going to be a large amount of work! Aside from that, I have started putting together a gallery of `Jupyter Notebooks` to show off some cool techniques/tricks I have learned in recent months. The first of these is what my team and I are calling "HP Bars" - below is a sneak peak at them (the notebook will show how to automatically do this with `panel` + `pandas`!). The idea is simple - show a colorbar in a button/tab that represents a categorical breakdown of the data contained within. This is just a small way of providing high level insight when you need to present many tabs of data and need to hone in on specific pieces.

Check out the sample below and keep an eye on the [gallery](https://github.com/NESWare/gallery), which is where I will start throwing some code into! 

### HP Bar Sample

Here we have some tables containing the numbers 1-27. We highlight <font color="green">prime numbers</font>, <font color="orange">perfect squares</font>, and <font color="red">perfect cubes</font>. While this is absolutely contrived, if for instance we wanted to look at the group with the most perfect squares, we can see based just on the tab that `Data 1` is where we should look. We use this at our analysis meetings to focus in on tabs (groups of data) that contain high numbers of deltas in our regression analysis. Not only is it very useful, it is even easier to implement!

<div class="tab">
  <button class="tablinks" onclick="showData(event, 'Data 1')" style="background-image: linear-gradient(90deg, green 44%, orange 44% 66%, red 66% 88%, white 88%); background-position: 0% 100%; background-size: 100% 20%; background-repeat: no-repeat;"  id="defaultOpen">Data 1</button>
  <button class="tablinks" onclick="showData(event, 'Data 2')" style="background-image: linear-gradient(90deg, green 33%, orange 33% 44%, white 44%); background-position: 0% 100%; background-size: 100% 20%; background-repeat: no-repeat;" >Data 2</button>
  <button class="tablinks" onclick="showData(event, 'Data 3')" style="background-image: linear-gradient(90deg, green 22%, orange 22% 33%, red 33% 44%, white 44%); background-position: 0% 100%; background-size: 100% 20%; background-repeat: no-repeat;" >Data 3</button>
</div>
<hr>
<div id="Data 1" class="tabcontent">
  <h4>Data 1</h4>
  <table style="text-align:center">
    <thead>
      <tr>
        <th>Col1</th>
        <th>Col2</th>
        <th>Col3</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style='color:white; background-color:red'>1</td>
        <td style='color:white; background-color:green'>2</td>
        <td style='color:white; background-color:green'>3</td>
      </tr>
      <tr>
        <td style='color:white; background-color:orange'>4</td>
        <td style='color:white; background-color:green'>5</td>
        <td>6</td>
      </tr>
      <tr>
        <td style='color:white; background-color:green'>7</td>
        <td style='color:white; background-color:red'>8</td>
        <td style='color:white; background-color:orange'>9</td>
      </tr>
    </tbody>
  </table>
</div>
<div id="Data 2" class="tabcontent">
  <h4>Data 2</h4>
  <table style="text-align:center">
    <thead>
      <tr>
        <th>Col1</th>
        <th>Col2</th>
        <th>Col3</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>10</td>
        <td style='color:white; background-color:green'>11</td>
        <td>12</td>
      </tr>
      <tr>
        <td style='color:white; background-color:green'>13</td>
        <td>14</td>
        <td>15</td>
      </tr>
      <tr>
        <td style='color:white; background-color:orange'>16</td>
        <td style='color:white; background-color:green'>17</td>
        <td>18</td>
      </tr>
    </tbody>
  </table>
</div>
<div id="Data 3" class="tabcontent">
  <h4>Data 3</h4>
  <table style="text-align:center">
    <thead>
      <tr>
        <th>Col1</th>
        <th>Col2</th>
        <th>Col3</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style='color:white; background-color:green'>19</td>
        <td>20</td>
        <td>21</td>
      </tr>
      <tr>
        <td>22</td>
        <td style='color:white; background-color:green'>23</td>
        <td>24</td>
      </tr>
      <tr>
        <td style='color:white; background-color:orange'>25</td>
        <td>26</td>
        <td style='color:white; background-color:red'>27</td>
      </tr>
    </tbody>
  </table>
</div>

<script>
function showData(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
document.getElementById("defaultOpen").click();
</script>
