package testnlpcapture;
import java.io.BufferedReader;
import java.util.regex.Pattern;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.util.Scanner;

public class reader {
	
	public static void main(String args[]) throws IOException{	
		 createTestCountFiles(new File("C:\\Input Folder"), "C:\\Output Folder");
	}
	
	public static void createTestCountFiles(File dir, String newPath) throws IOException {

        File newDir = new File(newPath);
        if (!newDir.exists()) {
            newDir.mkdir();
        }

        for (File file : dir.listFiles()) {
            int count = lineCount(file.getPath());
            File newFile = new File(newPath+"/"+file.getName());
            if (!newFile.exists()) {
                newFile.createNewFile();
            }
            try (FileWriter fw = new FileWriter(newFile)) {
                fw.write("" + count + "");
                System.out.println(newFile);
                System.out.println(count);
            }
        }
    }
	
	private static int lineCount(String file) throws IOException  {
		String word1 = "for";

	    int wordCount = 0;
	    
	    Scanner sc = new Scanner(new File(file));
	    while(sc.hasNext()){
	    	
	    	if (sc.next().equals(word1)){
	        	wordCount++;
	        }
	    }
	    
	    return wordCount; 
    }
	
}




  

    

    
