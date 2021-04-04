#include <bits/stdc++.h>

using namespace std;

void solve() {
    int n, k, d, s;
    cin >> n >> k >> d >> s;
    // s * k + x * (n - k) = d * n
    // x = (dn -sk)/(n-k)
    int numer = d * n - s * k;
    int denom = n - k;
    if (0 <= numer && numer <= 100 * denom) {
        double x = (double) numer / denom;
        cout << setprecision(10) << x << "\n";
    } else {
        cout << "impossible\n";
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    solve();
    return 0;
}