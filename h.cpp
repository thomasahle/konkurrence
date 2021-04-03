#include <bits/stdc++.h>

using namespace std;

void solve() {
    int n;
    cin >> n;
    vector<int> xs(n);
    for (int& x : xs) {
        cin >> x;
    }
    sort(xs.begin(), xs.end());
    for (int i = n - 1; i >= 0; --i) {
        int j = i % 2 == 0 ? n - 1 - i/2 : i/2;
        cout << xs[j] << " ";
    }
    cout << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    solve();
    return 0;
}
