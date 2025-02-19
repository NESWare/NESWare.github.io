title: Discord for a GitHub Classroom - Part 0
date: 2020-04-15
tags: storytime software education
readtime: 7
---fm---

This post is the first (a prologue, really) in a series documenting my journey as an educator and the development of a Discord Bot that I plan on using to manage a classroom. Specifically, this post details the motivation behind what I have been working on and how I arrived to where I am now in 2020. There is nothing technical here, so feel free to give this one a hard pass if that is what you are looking for.

#### Other Articles in this Series

* [Part 0 - Background & Motivation](/2020/04/15/discord-github-classroom-pt0.html) (you are here!)
* [Part 1 - GitHub App Basics](/2020/04/26/discord-github-classroom-pt1.html)

## Learning to Teach is Hard

I have been fortunate enough to be able to teach at my local university for nearly 9 years now. I started teaching for the physics department while I was still in graduate school; I was an instructor for the lab sections for Intro to Physics 1. I eventually started teaching full lectures, and due to some dumb luck, I found myself teaching C++ for the *mathematics* department (yes, the mathematics department). I was still young and still very much inexperienced. I had a solid grasp on C++, but I did not quite have a solid grasp on software, and even less so software education. I also did not go to school for software, and so the course was odd to say the least. The class itself is titled "Scientific Computing with C++" - a one semester crash course on the C++ language *assuming zero background in software or computing* (it is a math class, after all). All I knew going into this is how I learned how to code: reading a book and just doing things myself. The course is hard to teach because I have students with zero coding experience and others with plenty. Ensuring that the course is challenging enough for the newbies and not too easy for the seasoned coders is massively difficult and something I still struggle with today. But I digress...

### The Beginning

When I started teaching this class in 2015, I relied on severely inefficient means to teach a software class: slide decks, printouts, emails, printed assignment submissions, etc. This is how I taught some of my other lectures, and so it seemed only natural to do the same here. Things were clunky but fared OK. 2016 was a little simpler as I was able to reuse and improve on material from the previous year and 2017 was poised to be even better.

Sadly, as I arrived at year 3 the material felt extremely stale. In retrospect, the material was always stale, but it was then that I had more experience with software end-to-end. How could I introduce more software concepts into the class? How could I improve the grading process? Grading was a sore point for me. *That is because grading sucks*. When you need to look at the same piece of code dozens of times over, and everyone has a different coding style (or no style at all) with a different take on the solution, you spend *a lot* of time grading. My focus for year 3 was to make a much heavier use of the learning management system (LMS) provided by the university and to figure out how I could improve the grading process.

### Struggling to Find a Better Way

The 2017 semester led me down two paths: learning how much I hated the LMS we had access to and how easy grading software can be. The LMS provides features for making announcements and managing grades but managing course material and assignment submissions was a nightmare for both the students and me. The best part about it all was being able to download their assignments as one large zip file.

I still needed an answer for how I could simplify grading. I began writing my assignments to dictate very specifically what their program output should be and how it should be formatted. This allowed me to write scripts to run their programs and validate the output: if their output matched mine, character for character, then I knew that the assignment was done correctly. I stopped caring about coding style, as in the end it was too hard to enforce (and it is a highly opinionated topic). Grading assignments went from a multiple-hour ordeal to maybe an hour at most. Obviously if someone's output did not match mine, I would need to investigate their code and see what was going on, but for anyone who did things correctly I was able to grade their assignment with effectively zero effort.

The 2017 iteration in the end was not so great. I stretched myself far too thin with enrolling in another graduate program and starting a new job; I was hardly able to improve on anything I was doing for the course. I still relied heavily on the same LMS that was failing me before and I only made marginal improvements on grading. All the while I was trying to rewrite my material to emphasize modern C++ techniques and practices. This spelled out a disastrous semester.

I had high hopes for 2018, but again stretched myself far too thin with starting yet another new job. By this point in time I was finally starting to learn Git and GitHub (I had only ever used ClearCase and Perforce). GitHub blew my mind and I thought to myself *this is what I need to use*. I made use of GitHub and GitHub Classroom to manage all assignments and developed a configurable and reusable testing tool so that students could test and "self-grade" their work. The process was finally getting better but much more was needed.

### Doing it Right

Finally, we arrive at 2019. I abandoned the LMS outside of its gradebook feature and was otherwise 100% using GitHub. Notes were uploaded to repositories that students could access. I also provided code samples and had plenty of assignments for students to practice with. Assignments were distributed and collected via GitHub Classroom and announcements were given via GitHub. The self-grading tool was more advanced than it had ever been, and outside of my own issues with writing bug-free assignments, things went far better than I had hoped. Most assignments had a visualization component using Python so that they could *see* the results of our programs. It was a lot of work and not without its issues, but I finally had done something I felt was *good*.

Every assignment now comes with a fully detailed readme, all necessary starter code, a fully featured Makefile for building and testing code (using the grading tool), and prebaked visualization components if appropriate. The Fall 2020 semester will also include autograding and feedback via GitHub Classroom. This is 90% of everything I could possibly want.

### Looking Forward

What the rest of this series will detail is that other 10%. I want a more seamless means of communication with my students and I want to build a collaborative culture within the class. I want students to not only come to me with questions, but also go to each other with questions. I also want them to be able to interact dynamically with all course material and be able to view their assignments and grades. *I want Discord to be my learning management system*.
