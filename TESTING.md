BUGS 

**BUG**: When I ran the server, received the following error:

 File "/Users/vikimulhall/GAA_STORE/products/views.py", line 1, in <module>
    from django.shortcuts import renderget_object_or_404
ImportError: cannot import name 'renderget_object_or_404' from 'django.shortcuts' (/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/django/shortcuts.py). Did you mean: 'get_object_or_404'?

**RESOLVED BY**: Went to my views.py file and saw I had a typo in the import line. Amended and started server again. 

**BUG**: After adding the the hurley page, it wouldn't display and sent the following error in the terminal:

Not Found: /hurleys/
[25/Apr/2025 15:06:51] "GET /hurleys/ HTTP/1.1" 404 2717

**RESOLVED BY**: Realised I had forgotten to include the products app in the main urls.py. I then also included the hurling page itself. 

 **BUG**: Hurley images not being displayed & not consistent size.  
 **RESOLVED BY**: Changed location of images to the static folder, restarted server, only the ash image displayed, checked for typos, found dashes rather than hyphens, ameneded in the html page and resolved problem. To fix the inconsistent size of the ash hurley image compared to the other two, I added some css, which did not work, so I fixed the image again in canva and resaved and loaded and it worked when refreshed. 

 **BUG**: Created a hurling calculator, when the user enters the measurement in cms it will give the result in inches. On testing when I entered a number, no result was displayed. 
 **RESOLVED BY:** Checked the css and js and it seemed ok. Went to inspector tools and found the error that the converter.js was not found.  Realised I had spelled the converter.js file incorrectly in the directory. 

 ![converter js file spelled incorrectly](https://github.com/user-attachments/assets/20099172-ae50-45a4-9572-e1b82df89405)


 **BUG**: Creating a horizontal line to divide the helmet from hurley measurement section. 
**RESOLVED BY:** Checked using inspection tools, the width appeared as 0.  When I googled it, this can be an issue with flexbox layouts.  Applied some width in css and the issue was resolved. 
 
<img width="1264" alt="horizontal line bug no width" src="https://github.com/user-attachments/assets/f368d998-8f43-4d60-95d1-596241266d7b" />

 **BUG**: Creating a FAQ page, for better UX I wanted to to list the FAQ and if you click on the question it expands, so I used boostraps data-toggle accordian feature.  When I started the server it just displayed the question and the answer and had no toggle feature. 
 **RESOLVED BY:** I opened my development tools and checked my console and when I clicked on a question it displayed an error message. The error message indicates that in my collapse.js, something is null where an object is expected. This error can happen if you try to operate on an element that doesn't exist on the page.
I had put my converter calculator script into my base.file, which I should of kept in my how_to_measure.html file as base.html shares with everything else including my FAQ page.  I put my script files in base.html into the correct order.  I also reviewed my FAQ html structure as this can cause errors too. I restarted the server and now it is working. 

<img width="1217" alt="JS null error FAQ bug" src="https://github.com/user-attachments/assets/46484b58-2f93-403a-ab17-fe7b67a48b16" />

**BUG:** After fixing my FAQ bug, I checked to see if my converter calculator works and even though I entered a valid number is sent the error message that I entered an invalid number.  
**RESOLVED BY:** I opened up my inspector tools and could not see any error messages. Then reviewed my script on my html page and realised I put it in the wrong place, amended it and converter calculator working again. 


**BUG:** ValueError at /products/. The 'image' attribute has no file associated with it. After adding some test products through my django admin panel, when I ran the server this error was displayed. 
**RESOLVED BY:** I had come accross it in the walk-thru also, so I added a default-image.jpeg to my static files and put an if else option in my product_list.html to use the default if no prodcut img present. I will fix the image files but I just wanted to review the layout before committing to data. 


**BUG:** On my views.py file I had a red underline and when I right clicjed it said - Unable to import 'django.urls'PylintE0401:import-error. 
**RESOLVED BY:** I knew I had installed django but checked again by typing pip show django in the terminal. I could see my virtual env was running. I opened up setting in my VS code and updaed my pylint settings.  This worked and cut down on my errors to do with importing so that I could concentrate on the remaining. 

**BUG:** I needed to modify my model, as I wanted the user to be able to choose which manufacturers hurley they wanted. So  I created a new model and deleted it from the hurley model. I thought I had made migrations and run migrations but I obviously did something wrong and ended up with countless errors after errors for a day saying my table already existed but they didn't.
**RESOLVED BY:** Walking away from the laptop and returning. The advice I was getting on-line was to delete all previous migrations and reapply them, which I did but didn't solve the problem.  Ran my models.py though perplexity and was shown I had manufacurers in my grips which I shouldn't have had, amended that.  Stack overflow advised to delete my database, which I did and then reapply migrations which I did and it worked then. 

**BUG:** I realised that should of used a general product_detail.html rather than separate product detail pages to reuse code and work with the product list dynamically. So I set about to do that. REceived an error page NoReverseMatch at /products/hurley/1/. Reverse for 'add_to_bag' with arguments '('',)' not found. 1 pattern(s) tried: ['bag/add/(?P<product_id>[0-9]+)/\\Z']. 
**RESOLVED BY:** I fixed a typo in my nested form. I reviewed by views, concentrating on hurley_details as this was hightlighted in grey in the error page. In my return render I changed 'hurley': hurley.product to 'product': hurley.product and this fixed it. 


**BUG:**  When checking my products were displaying, I noticed that grips was not displaying a color drop down arrow, which it should have. 
**RESOLVED BY:**  Checked by def grip_detail view which looked correct, checked my grips model which also looked correct. After checking my product list template, I had a naming typo error which I corrected and I was missing the logic for grips, I added the condiation to check if it was a grip to render the color dropdown, which resolved the bug. 

**BUG:** Spent the day trying to get my bag to display anything, after adding items to it. 
**RESOLVED BY:** I had a few issues which got me into a lot of checks and rechecks.  My product_key and product_id were conflicting in my context-processor.py and views.py file. I wasn't iterating through my products correctly in my bag.html file. After fixing these errors it finally displayed the items on the table. 

**BUG:** When bag displayed, the product, description were not being displayed. 
**RESOLVED BY:** Added product under bag_contents in views.py and it displayed. 

**BUG:** I wanted to create a 'Gift Message'function.  So in the bag.html, I created a tickbox and a message box. If the box was ticked the user could write a gift message. But when the box was ticked, I couldn't write in the box. 
**RESOLVED BY:**  I checked my js code and it seemed ok. When I opened but my console and clicked on the tick box, nothing was happending so I figured the js and event listener were not being called. I removed the js code from the bottom of the bag.html and created a specific js file for bags app under the static folder as I thought the base.html and its scripts could be affecting it. Finally I changed {%block postloadjs %} to {% block extra_js %} and this  fixed it.   

**BUG:** Order Summary not displaying on checkout page. 
**RESOLVED BY:**  I learnt a lot with this bug. Firstly I had not imported my context-processors file correctly into my checkout views. Fixed that, but no resolution. Checked my views.py and context processors, checked my product models, checked my html. Everything looked ok. Put debugging statements in the checkout views, which displayed the correct output in the terminal, so that was working. Thenb put debugging statemtnts in the context_processors and that verified that my grand total was working, then I put debugging statements in my html, activated the server and went to checkout and right clicked to view page source - and all my products were listed there. After hours and hours of trying to fix this error, I put my cursor over the order summary as if to hgilight and realised it was white text on a white background! I may have cursed a little. Added some css to my base.css file and finally all was fixed.


**BUG:** Billing & Shipping field input narrow and not taking up full width
**RESOLVED BY:**  It appeared like this was due to some conflicting css rules. I checked base.css to see if there were any .form-control rules, but there were not.  I applied them to checkout.css but nothing changed.  I used !important beside it but still no luck. I ensured the checkout.css for the checkout page was loading by inspecting it in chrome developer and checking the network tab, yes that was loading. I checked the html form was inside the .col -md-6. I thought the fields were constained by bootstrap but in the end it was by their own css, so I targeting each element of the form field putting !important beside them, checkout-form imput, select and text area.  Finally this worked but then my tick boxes got misalighned. So I updated the css again to apply width of 100% to only text-based inputs. Finally sorted. 

**BUG:** Setting up stripe, I could not input anything in the card number field. 
**RESOLVED BY:** After spending a day and half, debugging, firstly I had a form nested within a form, which was incorrect. Fixed that. Checked css and any parents that might be having an effect. I added debugging to the stripe_elements.js and found that they weren't being loaded in the console. I had the script tag in my checkout.html I had {%block postload_js %} rather than {%block extra_js %}. After I did that I could see it in my console but it was showing a 404 error.  My settings.py were fine, with regards my static files, and I had listed checkout under apps. But it was file path was incorrect. I fixed that and finally it was resolved. 

UNRESOLVED BUG
**BUG:** Bag contents table not responsive on Firefox but perfect in Chrome.
**ATTEMPTED FIXES:** After looking on the net, this seems to be a common proble. Stack overflow suggested a fieldset and nest table within it, no luck, tried custom css, still no luck, reviewed code for errors and all seemed to be ok. Deleted custom css code and fieldset and no change.  I have spent a few hours trying to fix and need to step away from it now. I will try to revert back again if I have time. 
