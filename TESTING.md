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







