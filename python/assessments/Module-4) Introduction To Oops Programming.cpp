#include <iostream>
#include <string>

using namespace std;

class Lecturer
{
public:
    string name;
    string subject;
    string course;

    void input()
    {
        cout << "Enter Lecturer Name : ";
        getline(cin, name);

        cout << "Enter Subject Name  : ";
        getline(cin, subject);

        cout << "Enter Course Name   : ";
        getline(cin, course);
    }

    void display()
    {
        cout << "Lecturer Name : " << name << endl;
        cout << "Subject Name  : " << subject << endl;
        cout << "Course Name   : " << course << endl;
        cout << "-----------------------------" << endl;
    }
};

int main()
{
    Lecturer L[5];

    cout << "Enter Lecturer Details\n";
    cout << "=======================\n";

    for (int i = 0; i < 5; i++)
    {
        cout << "\nLecturer " << i + 1 << endl;
        L[i].input();
    }

    cout << "\nAll Lecturer Details\n";
    cout << "=======================\n";


    for (int i = 0; i < 5; i++)
    {
        cout << "\nLecturer " << i + 1 << endl;
        L[i].display();
    }

    return 0;
}
