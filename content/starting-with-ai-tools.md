---
title: Starting with AI Tools
date: 2026-03-06
tags: [Dev]
---

Last fall, I took paternal leave. When I left, AI for software development still felt like a toy. However, when I returned, the world had changed and the AI coding tools were ready for production. I realized I was behind the times and had to catch up.

At BYU-Idaho, I encourage students to develop portfolios of their technical work for use in their job and internship interviews. I decided to create this blog so that I could practice what I preach and have a portfolio to show the students.

I'm a dad, and finding time to write code on top of my other responsibilities has been difficult. As my personal, professional, and community responsibilities have grown, side projects have fallen by the wayside. If I could find a way to shorten the development cycle, then that could bring coding back into my life again.


To achieve all of these objectives, I started building this blog framework with AI tools. I'm a command-line guy, and chose to start with Google's Gemini CLI. That first day, I was elated. I was no longer using AI to work with individual files in a chat window, but I was directing changes across multiple files; it felt more like doing a code review. My heart is with the terminal, and it was so great to have access to one of the greatest tools ever invented without having to do anything crazy to my Vim configuration. I am a happy man!

![Gemini CLI in Terminal](assets/images/gemini-cli.png)

I'm building this site the same way I would build an application by hand. I start with a minimum viable product (MVP) and then make incremental changes from there. I commit to the Git repository often, so I can roll back changes as needed. After creating the initial site ([see Gemini CLI's post](generated-by-gemini-cli.html)), I have worked with Gemini CLI to add [additional features](https://github.com/seancrosby/blog/commits/main/), including:

* tags
* embedded images
* embedded videos
* unit tests
* additional pages
* HTML header reuse

There will be more features as well.

Using AI tools has leveraged my existing skills (code design and review) while also buying me great efficiency gains.

On a humorous note, when I asked Gemini CLI to add support for embedded YouTube videos, the video it added to my "hello world" post was Rick Astley's "Never Gonna Give You Up." AI Rickrolled me!

![Rickroll](assets/images/never.png)

