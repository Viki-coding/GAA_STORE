# GAA_STORE

Live Link:

Link to Kanban Board:

Table of Contents
Introduction
Description - Project Purpose
User Demographics - Target Audience
UX
User Stories
Design Choices
Typography
Wireframes
Flow Chart
Features
Interaction Points
Future Implementation Section
Accessibility
Technologies Used
Frameworks, Libraries and Programs Used
Deployment Steps
How to Fork
How to Clone
Heroku Deployment
Acknowledging Contributions & Credits
Media/Images
Content
Legal & Ethical Compliance

Introduction


Description - Project Purpose




CRUD
Create


Read


Update


Delete


User Personas - EXAMPLE:

e.g. Facilitator Fiona (Event Facilitator)
Demographics: 35 years old, runs a local parent-and-toddler group, volunteer.

Tech Savviness: Reasonably comfortable with technology, uses a computer for basic tasks.

Needs & Goals: Promote her parent-and-toddler group, easily create and manage event listings, reach a wide audience in the community, needs a user-friendly platform for event management.

Frustrations: Finds it time-consuming to promote her group through multiple channels, needs a central place to update event information, struggles with complicated website interfaces.

Website Use Case: Creates new event listings with detailed information (date, time, location, age group), updates existing listings, checks the number of bookings, interacts with community members through the website through email and phone.

Quote: "I need a simple way to let people know about our group and manage our events without spending hours on it."

Community Committee Member (Event Facilitator)
Demographics: 55 years old, Community Centre Committee Member, manages various hall events.

Tech Savviness: Moderate tech skills, delegate if possible.

Needs & Goals: Effectively promote all events, delegate event creation, manage event schedules and bookings, needs a reliable platform for event organization.

Frustrations: Coordinating multiple facilitators, ensuring all events are properly promoted, keeping track of bookings and schedules, managing user accounts and permissions.

Website Use Case: Oversees all event listings, manages facilitator accounts, checks overall website traffic and engagement, ensures the website is up-to-date and informative.

Quote: "I need a system that allows me to keep an overview of all the activities in the community centre and to easily delegate tasks."

Kanban Board

I found the Kanban very helpful, it did take time to set up, it was well planned and structured. I sometimes have a tendency to go from one area and then get distracted to start fixing another area, having the Kanban board with the user stories and the tasks that I needed to perform helped me to keep a structured approach to coding. I learnt that at the end of a commit if I put "relates to #1" etc it would be documented with the task # in my project. Live link at top of readme and made public.

Kanban Board Progress

UX

When you land on our site it is immediately obvious what the site is and conveys the message of 



USER STORIES
#1 As a 


Design Choices

Colour Scheme


Using a colour contrast checked we checked which font colours stood out best against our base colours. All receiving good ratings. Graphic illustrated below:

Color-contrast-good

Typography
Font used is Roboto from Google Fonts. It is in the sans serif family, is clean with a modern appearance. It is dyslexic friendly helping with readability.

Wireframes
Wireframes

ER Diagram & Data Schema


FEATURES
Feature Title / Screenshot / Value to the User

Navigation Bar:

Login Feature If you already have a username and password you can log in easily to view your events. Once logged in the button changes to Log Out. When you go to log out an alert modul asks if you are sure you want to log out.

Nav-bar with logout modul

Sign Up Feature:

If you are a new user, it is easy to navigate to the Sign Up form, enter your details and password being set up within seconds, the 'Login' button changes to 'Log Out' and you have access to book events.

Nav Bar


Search by Category Feature:

Users who want to narrow down the search to certain events, such as a new parent in the area may want to only see events in the 'Parent & Toddler' section. When a facilitator creates a new event, they have the opportunity of associating it with a certain category. By clicking on the drop down arrow, a list of categories is displayed and when a category is selected only events listed under that category are displayed. Leaving the selection to 'All' displays all events, with the post recently created first.

Sort-by-category



FOOTER FEATURES:

Footer Features

We use the attribute rel="noopener noreferrer" in the anchor tages to enhance security and protect against security vulnerabilities.

The Eircode of centre is already linked to google maps the user can easily navigate to the centre by clicking on the Eircode, which opens in a new page.

Facebook and Instagram Features:

This allows the user to access the Ballinameela Community Centre socials in a new page.

Pagination Feature:

The latest events are posted first, to view older posted events the user can user the pagination links at the bottom of the page to easily navigate though the pages.

Security
In a world where cyber security threats are on the increase, inlcuding the awful affect the HSE hack had on our health care system, it is important to be mindful of security when creating an application.
As well as the rel="noopener noreferrer" in the anchor tags of our external links other security meausures in our app include:

Authentication and authorization of our users using django framework
Using the CSRF protection tokens in our forms
Error handling such as creating our 404 page
Using djangos password validators
Using djangos security middleware settings.
Only authenticated users can edit delete their booked events
Only authenticated facilicators can create, view, edit, delete their own events.

Interaction
Whenever a user interacts with our site, they get immeadiate feedback messages and confirmations.

When a user clicks on Book Event - a message is displayed to let them know their booking is successful:

Event Booked Successfully

Error Handling

404 Page
We have created a 404 page so that user of accidentally enters a typo in the address they get an opportunity to be redirected back to the home page: 404 page 
When a user attempts to book an event who’s capacity has already been reached, i.e. the event is already booked out, a message is displayed to let them know event capacity has been reached:


Future Implementation Section


Accessibility
This is a community website for everyone in the community to use. Accessibility of the site is very important.

(a) Semantic HTML elements were used to provide meaningful structure to the content.

(b) Keyboard Navigation ensures all interactive elements like the form fields and buttons are accessible via the keyboard.

(c) Using Text Alternatives using Aria labels to describe content were used to improve accessibility for screen readers.

(d) Colour Contrast: The colour pallet chosen has sufficient contrast against the background to be readable by users with visual impairments.

(e) All forms were accessible with associated labels to provide clear instruction and are navigable using keyboard.

(d) Alt attributes were used to describe any image content such as the logo and notice board image.

(e) Testing, we used WAVE a Web Accessible Evaluation Tool to analyse the page and made adjustments to the site to try to improve it. It passed the 

Wave Evaluation without errors.

WAVE:

WAVE evaluation results

Lighthouse Testing

Lighthouse test results

Color Blindness Simulator Tool:

Color Blindness simulator

Technologies Used
HTML
CSS -
JS -
Python
Django
Bootstrap
Heroku
Postgres Database
Frameworks, Libraries and Programs Used:
Balsamiq Wireframes - used to create wireframes
Git - version control
Visual Studio Code
Git Hub - To save and store the files for the website
Google Fonts - to import fonts onto the website
Font Awesome for iconography on website
Favicon.io - to create favicon
Coolors - checking colour pallets and their contrast abilities with fonts.
Berme.net - to reduce image sizes and convert to .webp
Canva - to create logo image
Am I Responsive - quick tool to check how responsiveness on various devices and creates display
Responsive tool - (https://responsivetesttool.com/)
Screen Shot of site on various screens (https://techsini.com/multi-mockup/)
JSHint to check JS code
Spell Check
Heroku
Django
Pylint
FigJam - to create ER diagram
Figma - to crate wireframes
Converting tabel to markdown (https://tabletomarkdown.com/convert-spreadsheet-to-markdown/)
Whitenoise

Deployment Steps

The site is Deployed using GitHub Pages
Login to GitHub
Go to the projects repository (https://github.com/Viki-coding/community)
Click on Settings
Select pages in the left navigation bar
From SOURCE dropdown select Deploy from a Branch
Under BRANCH from dropdown select Main Branch and SAVE
The site is now deployed but may take a few minutes to go live.
Return to CODE tab of Github repo and wait a few minutes for build to finish, refresh page. This will show on GitHub-pages to see active deployments.

How to Fork
Login to Github
Go to Project repository
Click the FORK button top right corner

How to Clone
Log into Github
Go to project repository
Click on the code button, select what want to clone HTTPS, SSH or GitHub CLI and copy the link.
Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory
Copy 'git clone' into the terminal and paste the link you copied in step 3. Press enter.

Heroku Deployment
Log on to Heroku (https://dashboard.heroku.com/apps)
Select “Create new app”
Name the app something unique
Choose Europe from the dropdown
Click ‘Create App’
Go to the SETTINGS tab first
In the ‘Config Vars’ section aka environment variables
In the KEY section type in PORT and the value section type in 8000 – add
IF you build a landmark project that doesn’t use a cred.json file you don’t need to set up config vars otherwise:

In the KEY section type CREDS (all capital letters) –
Go to workspace and copy the entire creds.json file and paste it into the value field and add.
To add other dependencies:

ADD BUILDPACK
Select Python – choose add
Select Node.js – choose add
NOTE: (Should be in this order, python first then node.js)
DEPLOY SECTION:

Click on the DEPLOY Tab
Choose the Githb deployment method
Confirm that you want to connect to GitHub, gitbub will request your password to connect.
Click in repo name and Search for your repository name and select connect.
Select Enable Automatic Deploys
Check Choose a branch to deploy is defaulted is MAIN
Click on Display Branch
App will build:

Wait until the message ‘App was successfully deployed’ is displayed,
Click on the view button

Acknowledging Contributions & Credits
TITLE OR DESCRIPTION SOURCE OF LINK CONTEXT



MARKDOWN:

Help with markdown, found this site usefule (https://www.markdownguide.org/basic-syntax/) and downloaded this extenstion to Visual Studio Code (https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one#table-of-contents)

We gained inspiration with the READ.me by watching the video 'Creating your first README with Kera Cudmore' on CI Chanel Lead Library on YouTube and also the video with Lane-Sawyer Thompson on CI Channel on YouTube. Thanks to the on-line tutor, Oisin and Rebecca for their expertise and ability to explain some of the 'challenges' I encountered. Thanks to our very supportive and positive facilitator Kay and my Kiwi mentor Dick Vlaanderen. Also found the webinar 'Community Q&A: How to Troubleshoot with Lane-Sawyer Thompson' very helpful approach to how to view looking at the site for bugs and methodically identifying issues.

Media/Images
Images of logo and notice board both created in Canva by myself using canva template. No other imagery used.

CONTENT
The content text for website is fictious and is written by Viki Mulhall.

Legal & Ethical Compliance
This project is for educational purposes only.