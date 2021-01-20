package camelproj;
import java.util.regex.Pattern;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.util.Scanner;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;

public class camelcase {
	
	public static void main(String args[]) throws IOException{	
		
		createTestCountFiles(new File("C:\\Input Folder"), "C:\\Output Folder");
			
	}
	
	public static void createTestCountFiles(File dir, String newPath) throws IOException {
		
		

        File newDir = new File(newPath);
        if (!newDir.exists()) {
            newDir.mkdir();
        }

        for (File file : dir.listFiles()) {
            ArrayList<String> linesofcode = lineCount(file.getPath());
            
            String formattedString = linesofcode.toString().toLowerCase()
            	    .replace(",", "\n")  //remove the commas
            	    .replace("[", "")  //remove the right bracket
            	    .replace("]", "")  //remove the left bracket
            	    .trim();           //remove trailing spaces from partially initialized arrays
            
            File newFile = new File(newPath+"/"+file.getName());
            if (!newFile.exists()) {
                newFile.createNewFile();
            }
            try (FileWriter fw = new FileWriter(newFile)) {
                fw.write("" + formattedString + "");
                System.out.println(newFile);
                System.out.println(linesofcode);
            }
        }
    }
	
	private static ArrayList<String> lineCount(String file) throws IOException  {
		
		ArrayList<String> codeline = new ArrayList<String> ();
	    
	    Scanner sc = new Scanner(new File(file));
	    Scanner sc2 = new Scanner(new File(file));
	    while(sc.hasNext()){    	
	    	LinkedList<String> eachline = splitCamelCaseString(sc.next());
	    	codeline.addAll(eachline);			    	
	    }
	    while(sc2.hasNext()){	
	    	String token1 = sc2.nextLine();
	        codeline.add(token1);   		    			    	
	    }
	    
	    return codeline; 
    }
	
	public static LinkedList<String> splitCamelCaseString(String s){
	    LinkedList<String> result = new LinkedList<String>();	
	    for (String w : s.split("(?<!(^|[A-Z]))(?=[A-Z])|(?<!^)(?=[A-Z][a-z])")) {
	    	result.add(w);
	    }    
	    return result;
	}
}

