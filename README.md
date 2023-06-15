# VICS-Gallery-Maker

Start of the project supported by [Fortech, Technologies pour l’investigation numérique](https://fortech.fr)  

## Description

This is a tool design to make a gallery from a VICS ([Video Image Classification Standard](https://www.projectvic.org/vics-data-model)) JSON Export.  
It produce something like this :  
<kbd><img src="https://raw.githubusercontent.com/lemnet/VICS-Gallery-Maker/main/pics//Result.png" alt="Result" width=400></kbd>
## How-to use

1. Export from [Analyse DI](https://www.griffeye.com/analyze-di/) (or any other tool that support VICS JSON Export) :  

<kbd><img src="https://raw.githubusercontent.com/lemnet/VICS-Gallery-Maker/main/pics/Export0.png" alt="Export step 0" width=400></kbd>  
  
<kbd><img src="https://raw.githubusercontent.com/lemnet/VICS-Gallery-Maker/main/pics/Export1.png" alt="Export step 1" width=400></kbd>  

<kbd><img src="https://raw.githubusercontent.com/lemnet/VICS-Gallery-Maker/main/pics/Export2.png" alt="Export step 2" width=400></kbd>  
(Select `VICS version 2.0` and tick `Export Files`)  
  
<kbd><img src="https://raw.githubusercontent.com/lemnet/VICS-Gallery-Maker/main/pics/Export3.png" alt="Export step 3" width=400></kbd>  

2. Run VICS-Gallery-Maker: 
    1. Select the json file by clicking the `...` button
        * If the file is OK, it will display `Json seems valid` and the total and unique numbers of files
        * If the file is not OK, it will display `Json doesn't seem valid`
    2. Change `files per line`, `font size`, `Max. dimension of pictures`, `Output all files`, if needed
    3. Select the fields to output
    4. Click `OK`

<kbd><img src="https://raw.githubusercontent.com/lemnet/VICS-Gallery-Maker/main/pics/Process.png" alt="Process" width=400></kbd>

3. The outputed html file automaticaly open in the default browser

4. Print it to a PDF ajusting the scale : 

<kbd><img src="https://raw.githubusercontent.com/lemnet/VICS-Gallery-Maker/main/pics/Result.png" alt="Result" width=400></kbd>

5. Enjoy

## Credit

Images from [wikimedia](https://commons.wikimedia.org)  
Written by [@lemnet_fr](https://twitter.com/lemnet_fr)  
