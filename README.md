# Extraction-of-vital-imformation-from-Driving-license-using-azure-vision-ocr

## API selection
As we have to do extraction of some information from an image. We need to use OCR(Optical character recognition ) technique to do the task , but as most of the open source OCR api’s are good enough to work with but they didn’t provide best results .So i decided to go with Microsoft azure cognitive vision ocr api  . First I used its OCR service after a while I realised that going with cognitive vision handwritten text recognition api might be more insightful because it's going to have some NLP algorithms within it as I worked with NLP a lot in the past .

<b> Final API selection : “azure cognitive vision handwritten text recognition api </b>

## Preprocessing of the Images:

### Resizing the Image:

As the dataset contains images of different sizes .So we have to resize all images to a constant because we have to apply a lot of coordinate relation between the different text within a single image. Otherwise it’s hard to handle with varying sizes.  

### Skewness Correction of textual alignment or correction of orientation of images:

Cognitive api provide you with feature(parameter) to find out the textual alignment by try to read the text from all 360 degree.

But the problem is that it doesn’t return the coordinates with new alignment , but it sends it in respect to the original due to which we have to first get the alignment angle then apply to it , then save it in your local computer, then pass it again. Otherwise we didn’t get aligned coordinates which is going to create problems in textual processing in the next step .

Other preprocessing techniques i used are blur smoothening , adaptive thresholding ,  Remove noise(Denoise) etc but i dont think these helped because of the fact vision api already uses these techniques.


### Methods

After that , If we make a call to api with an image it returns a json formatted file.

It provides you with the coordinates of corners of textual block  after plotting these block onto the image it looks like this.


Conditional statements between the coordinates :


After that there starts a long hours of defining conditional statements to get required text out of it .It cannot be possible to define those 50+ conditional statements here ( notebook), but you get the idea it is easy to get text out of it .


Textual processing:


A lot of textual processing requires such as splitting the words serpertly , removing the typos like(colon, commas etc) . Other than that there also defining the relationship between words include mapping such key(name)-value(name).


Result look like this in form of list:


After that we can use python pandas dataframe to convert the list formatted result into proper csv or excel format.After converting into csv or excel:


Accuracy:

In this particular case the a lot metric accuracy we can define , some of the following are:


Most simple one (but certainly the most harsh one):

Simply check whether all fields of single image matching the output or not , then classify it as 1 or 0

        

        Acc = Correct number of cases/Total number of cases

                



Most suitable:

Simply checking fields wise , how many time models are able to recognize the name or registration no.. etc correct. Then calculate the F1 score ,accuracy, precision ,recall based on that.

                

                Acc = (Total number of fields matched) / 6 X (total number of test cases)


Most complex ( give you the best depth analysis of accuracy)

Check character wise  , how many time models are able to recognize the character correctly at a particular location. Then calculate the F1 score ,accuracy, precision ,recall based on that.


                Acc = (Total characters matched) / (total number of character)

                



It depends on the metric you select but I think it will be able to achieve  90% percent unless the metric is harsh or  something like this.










