package serial_test;

class Container{

	  //eventually provides setters and getters
	  public String header;
	  public String body;
	  public String checksum;
	  public String message;
	  public boolean read;
	  //------------

	  private static Container instance = null;
	  private void Container(){

	  }
	  public static Container getInstance(){
	    if(instance==null){
	       instance = new Container();
	      }
	      return instance;
	  }
	}