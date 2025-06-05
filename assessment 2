#include<iostream>
using namespace std;

class Menu{ //this class have all menu and sub menu
		
		public:
			//display main menu
			mymenu()
			{
				cout<<"1) Pizzas "<<endl;
				cout<<"2) Burgers "<<endl;
				cout<<"3) Sandwich "<<endl;
				cout<<"4) Rolls "<<endl;
				cout<<"5) Biryani "<<endl;
			}
			//display submenu pizza
			submenu_pizza()
			{
				cout<<"Margherita Pizza...199/-"<<endl;
				cout<<"Farmhouse..........349/-"<<endl;
				cout<<"Cheese Burst.......279/-"<<endl;
				cout<<endl;
			}
			//display submenu burger
			submenu_burger()
			{
				cout<<"Veg Cheeseburger.......99/-"<<endl;
				cout<<"Paneer Burger..........129/-"<<endl;
				cout<<"Aloo Tikki Burger......89/-"<<endl;
				cout<<endl;
			}
			//display submenu sandwich
			submenu_sandwich()
			{
				cout<<"Veg Club Sandwich.........349/-"<<endl;
				cout<<"Paneer Tikka Sandwich.....299/-"<<endl;
				cout<<"Grilled Cheese Sandwich...249/-"<<endl;
				cout<<endl;
			}
			//display submenu rolls
			submenu_roll()
			{
				cout<<"Veg Frankie............99/-"<<endl;
				cout<<"Paneer Kathi Roll......149/-"<<endl;
				cout<<"Soya Chaap Roll........179/-"<<endl;
				cout<<endl;
			}
			//display submenu biryani
			submenu_biryani()
			{
				cout<<"Paneer Biryani..........249/-"<<endl;
				cout<<"Hyderabadi Veg Biryani..199/-"<<endl;
				cout<<"Dum Biryani.............149/-"<<endl;
				cout<<endl;
			}
};

class food:public Menu{
	public:
		int type; //which type of item want to order from submenu
		int quntity;// how many quntity want in order 
		int choice;// select from main menu which food do you want 
		int price; // submenu every item price 
		string item;// sub menu every item name
		order()
		{
			mymenu(); //display the main menu
			cout<<endl; 
		
		
		cout<<"Please enter your choice: "; //select from main menu which food do user want
		cin>>choice; // user choice
		cout<<endl;
	
	switch(choice) // based on user choice this will show user their menu
	{
		case 1:
			submenu_pizza();
			cout<<"Please enter which Pizza you would like to have? ";
			cin>>type;
			switch(type)
			{
				case 1:
					price=199; 
					item="Margherita Pizza";
					break;
				case 2:
					price=349;
					item="Farmhouse";
					break;
				case 3:
					price=279;
					item="Cheese Burst";
					break;
				default:
					cout<<"Invalid"<<endl;
					break;
			}
			break;
		case 2:
			submenu_burger();
			cout<<"Please enter which Burger you would like to have? ";
			cin>>type;
			switch(type)
			{
				case 1:
					price=99;
					item="Veg Cheeseburger";
					break;
				case 2:
					price=129;
					item="Paneer Burger";
					break;
				case 3:
					price=89;
					item="Aloo Tikki Burger";
					break;
				default:
					cout<<"Invalid"<<endl;
					break;
			}
			break;
		case 3:
			submenu_sandwich();
			cout<<"Please enter which Sandwich you would like to have? ";
			cin>>type;
			switch(type)
			{
				case 1:
					price=349;
					item="Veg Club Sandwich";
					break;
				case 2:
					price=299;
					item="Paneer Tikka Sandwich";
					break;
				case 3:
					price=249;
					item="Grilled Cheese Sandwich";
					break;
				default:
					cout<<"Invalid"<<endl;
					break;
			}
			break;
		case 4:
			submenu_roll();
			cout<<"Please enter which Roll you would like to have? ";
			cin>>type;
			switch(type)
			{
				case 1:
					price=99;
					item="Veg Frankie";
					break;
				case 2:
					price=149;
					item="Paneer Kathi Roll";
					break;
				case 3:
					price=179;
					item="Soya Chaap Roll";
					break;
				default:
					cout<<"Invalid"<<endl;
					break;
			}
			break;
		case 5:
			submenu_biryani();
			cout<<"Please enter which Biryani you would like to have? ";
			cin>>type;
			switch(type)
			{
				case 1:
					price=249;
					item="Paneer Biryani";
					break;
				case 2:
					price=199;
					item="Hyderabadi Veg Biryani";
					break;
				case 3:
					price=149;
					item="Dum Biryani";
					break;
				default:
					cout<<"Invalid"<<endl;
					break;
			}
			break;
		default:
			cout<<"Enter a valid choice";
			break;
	}
	// take quntity from user 
	cout<<endl;
	cout<<"Enter a quantity ";
	cin>>quntity;
	
	cout<<endl;
	
	int total = price*quntity; // makeing bill for user
	cout<<quntity<<" "<<item<<endl; // printing quntity and item name that user will buy
	cout<<"Your Bill is"<<total<<endl;  // giving user bill
	cout<<"your order will be ready in 40 minutes"<<endl<<"Thankyou for ordering from our center"<<endl;	
}
};


main()
{
	cout<<"\t\t\t\t-----------Fast Food-----------\t\t\t"<<endl;
	string name; // for user name
	char ch; // if user want to buy any otherthing it will be given choice
	//entry section
	cout<<"Enter your name: ";
	cin>>name;
	cout<<"Hello "<<name<<"!!"<<endl;
	cout<<endl;
	cout<<"What would you like to order?"<<endl;
	cout<<endl;
	//menu section
	cout<<"\t\t\t\t-----------Menu-----------\t\t\t"<<endl;

	//make object and call
	food obj;
	obj.order();
	
while(1)
{
	cout<<"Would you like to order anything else? Y/N: ";
	cin>>ch; 
	cout<<endl;
	
	if(ch =='y' || ch =='Y') //if user say yes print full menu via objact
	{
		obj.order();
	}
	else
	{
		cout<<"Thankyou"<<endl; // if user write no it will exit the program 
		break;
	}
	cout<<endl;
}
	
	
}
