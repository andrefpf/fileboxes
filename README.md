<div align="center">
  <img width="100" src="https://github.com/user-attachments/assets/08d8ef52-9c58-41a3-b9b8-ef53be0ee1b7" alt="ExpiraBot Logo" align="center">
</div>
<h1 align="center" style="margin-top: 20px;"> Fileboxes </h1>

# Why it exists? 
A common feature in most popular software is to allow the user to save the project in a file to continue the work latter or to send it to someone.
If you find yourself in the position to create the said file you may have found the following solutions (and associated problems):
- Create a single JSON file with all the configurations needed

    A good solution, but not very scalable and flexible (specially if you need to deal with images or custom file formats).

- Create your own binary format

    Please, don't. Except if you really need.

- Create a zip file encapsulating everything you need.
    
    Yeah, that is a good option.
    Microsoft does it with Office Open XML (Used in Word, Excel and Power Point).
    The problem with it is that it uses mainly XML files, that were a good idea 30 years ago, but we can move on to more readable formats.

- Filebox

    Great choice. It just zips the stuff you need, but using an easy pythonic API to simplify your life.


# Examples
![WIP](https://cdn-icons-png.flaticon.com/512/5229/5229377.png)
