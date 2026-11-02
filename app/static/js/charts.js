// Dynamic Chart.js Analytics Loader
document.addEventListener('DOMContentLoaded', () => {
    const monthlyCanvas = document.getElementById('monthlyActivityChart');
    if (!monthlyCanvas) return; // Not on dashboard page

    // Fetch dynamic JSON data from backend SQL queries
    fetch('/api/charts')
        .then(response => {
            if (!response.ok) throw new Error('Network error loading analytics');
            return response.json();
        })
        .then(data => {
            renderMonthlyActivityChart(data.monthly_activity);
            renderDepositVsWithdrawalChart(data.deposit_vs_withdrawal);
            renderAccountTypeChart(data.account_type_distribution);
            renderRegistrationTrendsChart(data.customer_registration_trends);
            renderBranchBalanceChart(data.branch_wise_balance);
            renderLoanDistributionChart(data.loan_distribution);
        })
        .catch(err => {
            console.error('Failed to load chart analytics:', err);
        });
});

// Chart 1: Monthly Transaction Activity
function renderMonthlyActivityChart(data) {
    const ctx = document.getElementById('monthlyActivityChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels.length ? data.labels : ['No Data'],
            datasets: [
                {
                    label: 'Volume (₹)',
                    data: data.volumes,
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: '#2563eb',
                    borderWidth: 1.5,
                    borderRadius: 6,
                    yAxisID: 'y'
                },
                {
                    label: 'Tx Count',
                    data: data.counts,
                    type: 'line',
                    borderColor: '#f59e0b',
                    backgroundColor: '#f59e0b',
                    borderWidth: 2.5,
                    tension: 0.3,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    ticks: {
                        callback: val => '₹' + (val >= 1000 ? (val/1000).toFixed(0) + 'k' : val)
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}

// Chart 2: Deposit vs. Withdrawal
function renderDepositVsWithdrawalChart(data) {
    const ctx = document.getElementById('depositWithdrawalChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.amounts,
                backgroundColor: ['#10b981', '#ef4444'],
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.label}: ₹${ctx.parsed.toLocaleString('en-IN')}`
                    }
                }
            },
            cutout: '68%'
        }
    });
}

// Chart 3: Account Type Distribution
function renderAccountTypeChart(data) {
    const ctx = document.getElementById('accountTypeChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.counts,
                backgroundColor: ['#3b82f6', '#8b5cf6'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Chart 4: Customer Registration Trends
function renderRegistrationTrendsChart(data) {
    const ctx = document.getElementById('registrationTrendsChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'New Customers',
                data: data.registrations,
                fill: true,
                backgroundColor: 'rgba(99, 102, 241, 0.15)',
                borderColor: '#6366f1',
                tension: 0.35,
                borderWidth: 2.5,
                pointBackgroundColor: '#6366f1',
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 1 } }
            }
        }
    });
}

// Chart 5: Branch-wise Account Balance
function renderBranchBalanceChart(data) {
    const ctx = document.getElementById('branchBalanceChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Total Deposits (₹)',
                data: data.balances,
                backgroundColor: [
                    '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4'
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: {
                    ticks: {
                        callback: val => '₹' + (val >= 100000 ? (val/100000).toFixed(1) + 'L' : (val/1000).toFixed(0) + 'k')
                    }
                }
            }
        }
    });
}

// Chart 6: Loan Distribution
function renderLoanDistributionChart(data) {
    const ctx = document.getElementById('loanDistributionChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Loan Amount (₹)',
                data: data.amounts,
                backgroundColor: '#f43f5e',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    ticks: {
                        callback: val => '₹' + (val >= 100000 ? (val/100000).toFixed(1) + 'L' : val)
                    }
                }
            }
        }
    });
}
