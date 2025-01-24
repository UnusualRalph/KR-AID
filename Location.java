public class Location{
	//@author Rothang Ralefaso
	// 31-12-2024
	String street , town , city , province ;
	int zipcode,postalcode;

	public Location(){
		street=null;
		town= null;
		city = null;
		province = null;
		zipcode=0;
		postalcode=0;
	}


	public Location(String street ,String town,String city , String province ,int zipcode , int postalcode){
		street =street;
		town = town;
		city = city;
		province = province;
		zipcode=zipcode;
		postalcode=postalcode;
	}

	public String toString(){
		String result  = province+"\n"+city+"\n"+town+"\n"+street+"\n"+"postalcode: "+String.valueOf(postalcode)+ "\n zipcode: "+ String.valueOf(zipcode);
		return result;
	}}