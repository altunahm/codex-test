import matplotlib.pyplot as plt

# Stil Ayarları
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#333333'


def create_custom_gantt():
    """Generate the denim production critical path Gantt chart."""
    # Senin listene göre revize edilmiş veriler (Sondan başa doğru sıralı - grafikte yukarıdan aşağı görünür)
    tasks = [
        "Final Inspection & Ex-Factory",
        "Finishing & Packaging",
        "Shadeband Approval",
        "Washing Process",
        "Inline Inspection",
        "Production Start (Sewing)",
        "Cutting & Risk Review",
        "Fabric & Trims In-house",
        "PP Sample Approval",
        "Size Set Sample",
        "Fit Sample",
        "Fabric Booking",
        "Development Sample",
    ]

    # Başlangıç haftaları (Proje 12 hafta sürüyor varsayımıyla)
    start_weeks = [11.5, 10.5, 10, 8.5, 8, 6.5, 6, 4, 5, 3.5, 2, 1.5, 0]

    # Süreler (Hafta cinsinden yaklaşık süreler)
    durations = [0.5, 1, 0.5, 2, 0.5, 2, 0.5, 1, 1, 1, 1.5, 0.5, 1.5]

    fig, ax = plt.subplots(figsize=(12, 6))

    # Renkler: Kritik olmayanlar gri, Kritik Üretim aşamaları Mavi, Riskli aşamalar Turuncu
    colors = [
        '#e74c3c',  # Final - Kırmızı
        '#34495e',  # Finish
        '#f39c12',  # Shadeband - Turuncu (Riskli)
        '#3498db',  # Washing - Mavi
        '#2ecc71',  # Inline - Yeşil
        '#3498db',  # Sewing
        '#95a5a6',  # Cutting
        '#8e44ad',  # In-house - Mor
        '#e67e22',  # PP Sample - Turuncu (Kritik Onay)
        '#95a5a6',  # Size Set
        '#95a5a6',  # Fit
        '#95a5a6',  # Booking
        '#95a5a6',  # Dev
    ]

    for i, task in enumerate(tasks):
        ax.barh(
            task,
            durations[i],
            left=start_weeks[i],
            color=colors[i],
            edgecolor='white',
            height=0.6,
            alpha=0.9,
        )

        # Hafta/Süre etiketi
        ax.text(
            start_weeks[i] + durations[i] / 2,
            i,
            f"{durations[i]}w",
            va='center',
            ha='center',
            color='white',
            fontsize=8,
            fontweight='bold',
        )

    # Başlık ve Eksenler
    ax.set_title(
        "DENIM PRODUCTION CRITICAL PATH (12 WEEKS CYCLE)",
        fontsize=14,
        fontweight='bold',
        pad=20,
        loc='left',
    )
    ax.set_xlabel("Timeline (Weeks)", fontweight='bold')
    ax.set_xlim(0, 13)
    ax.set_xticks(range(0, 14))
    ax.set_xticklabels([f'Week {i}' for i in range(0, 14)])

    # Izgara ve Temizlik
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.savefig('custom_critical_path.png', dpi=300)
    plt.close(fig)


def create_test_plot():
    """Generate a simple line plot to validate Matplotlib setup."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_title("Test Plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.savefig("test_plot.png")
    plt.close(fig)


if __name__ == "__main__":
    create_custom_gantt()
    create_test_plot()
