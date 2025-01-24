import java.util.*;
public class Entity{
	/*@author Rothang Ralefaso
	version 0.1
	12/2024*/



	time opening ,closing;
	Location position;
	String name ;
	double rating;

	public Entity(){
		name=null;
		position = null;
		opening=null;
		closing = null;
		rating =0.0;
	}


	public Entity(Location position , time opening , time closing , String name , double rating){
		position = position;
		opening=opening;
		closing = closing;
		rating =rating;
		name=name;
	}

	
}