#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

static inline double f(double u)
{
    return u*(1.0-u);
}

void Cplusplus_logistic(int N, vector<double>& u, double dt){
    // Parameters
    int T = 25;
    double u0 = 1e-5;
    // Discretization
    // Time stepping
    u[0] = u0;
    for(auto i = u.begin(); i != u.end(); ++i){
        *(i+1) = *i + dt*f(*i);
    }
    //return (u);    
}

int main()
{
    vector<double> u(1000, 0.0);
    double dt = 25.0/1000;
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
using std::chrono::duration;
using std::chrono::milliseconds;

auto t1 = high_resolution_clock::now();
double rounds=1e5;
for(int i=0; i<rounds; i++){
    Cplusplus_logistic(1000, u, dt);
}
auto t2 = high_resolution_clock::now();

/* Getting number of milliseconds as an integer. */
auto ms_int = duration_cast<milliseconds>(t2 - t1);

/* Getting number of milliseconds as a double. */
duration<double, std::milli> ms_double = t2 - t1;

std::cout << ms_double.count()*1000/rounds << "μs\n";
std::cout << ms_double.count() << "ms";

}
