public class time{

	/*the time class was written on 30-12-2024 
	@author Rothang Ralph Ralefaso
	@version 0 */

	int hours,mins,sec;
	 public time(){
	 	hours  = 00;
	 	mins = 00;
	 }

	 private time(int hours , int mins){
	 	hours = hours;
	 	mins = mins;
	 }



	public void setHours(int hours){
		hours = hours;
	}

	public int getHours(){
		return hours ;
	}
	public void setMins(int mins){
		mins = mins;
	}

	public int getMins(){
		return mins;
	}

	public String toString(){
		String str_hours = String.valueOf(hours);
		String str_mins  = String.valueOf(mins);

		return ( str_hours+" : "+str_mins);
	}}