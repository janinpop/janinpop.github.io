---
permalink: /
title: "Welcome to my personnal webpage"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---
I'm a post-doctoral researcher in **instrumental astronomy**, with a deep love for **physics**, **mathematics**, and **computers** — and an equally strong passion for **sport**.  
Whether I'm developing high-precision instruments or out trail running, climbing, or on a bike, I’m always chasing performance, balance, and new challenges.

This site brings together my professional work and the things that keep me curious (and moving).  
You’ll find:

- 📝 [Research papers](./publications/)
- 🎤 [Talks and presentations](./talks/)
- ⚙️ [Side projects & hobbies](./portfolio/)

Want to know more? [Check out my CV](./cv/), or [send me an email](mailto:pierre.janinpotiron@gmail.com).

---

<div id="quote-box" style="font-style: italic; margin-top: 2em;"></div>

<script>
  fetch('quotes.json')
    .then(response => response.json())
    .then(quotes => {
      const quote = quotes[Math.floor(Math.random() * quotes.length)];
      document.getElementById('quote-box').innerText = quote;
    })
    .catch(() => {
      document.getElementById('quote-box').innerText = '“Keep looking up.” – Unknown';
    });
</script>
\

<video controls loop muted autoplay preload="auto" src="../files/closed_loop.mp4" title="Title" width="750"></video>