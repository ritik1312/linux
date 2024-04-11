// DATATYPES AND INPUT - OUTPUT


import java.util.Scanner;   //package

// There is only one public class in a file with same name as name of file
public class practice1 {
    /* static functions of a class can be called without creating objects.
    They acquire memory once they are defined in class & shared access among objects */
    public static void main(String[] args) {
        System.out.println("Hello World");
        
        Scanner sc = new Scanner(System.in);
        //creating a scanner class object to scan the console input

        System.out.print("What is your name? : ");
        String name = sc.nextLine();
        // .nextLine() takes whole line input
        // .next() for a string input
        
        System.out.println("Hello "+name);
        
        System.out.print("What is your age? : ");
        int age = sc.nextInt();
        /* 
        .nextInt() for integer input
         Similarly .nextFloat(), .nextDouble()
        */

        System.out.println("Enter 5 integers : ");

        // array in Java are as objects
        int arr[] = new int[5];
        double sum=0;
        for(int i=0;i<5;i++)
        {
            arr[i] = sc.nextInt();
            sum+=arr[i];
        }
        System.out.println("The average of these numbers is : "+sum/5);

    }
}
