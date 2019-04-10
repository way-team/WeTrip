import { Component, OnInit, ViewChild } from "@angular/core";
import { TranslateService } from "@ngx-translate/core";
import { DataManagement } from "src/app/services/dataManagement";
import { Router } from "@angular/router";
import { Chart } from "chart.js";
import { Color } from "@ionic/core";

@Component({
  selector: "app-dashboard-detail",
  templateUrl: "./dashboard-detail.page.html",
  styleUrls: ["./dashboard-detail.page.scss"]
})
export class DashboardDetailPage implements OnInit {
  @ViewChild("barCanvas") barCanvas;
  @ViewChild("doughnutCanvas") doughnutCanvas;

  type = null;
  stats = null;
  barChart: any;
  doughnutChart: any;
  numberOfTrips = null;
  ratioOfPrivateTrips = null;
  percentagePrivateTrips = null;
  percentagePublicTrips = null;
  avgAppsPerTrip = null;
  numberOfUsers = null;
  percentageMen  = null;
  percentageWomen = null;
  percentageNonBinary = null;
  percentagePremiumUsers = null;
  percentageNonPremiumUsers = null;
  premiumUsersRatio = null;
  percentageActiveUsers = null;
  percentageDeletedUsers = null;
  activeUsersRatio  = null;
  avgTripsPerUser = null;
  avgLanguagesPerUser = null;
  avgRatingPerUser = null;



  configuration1 = {
    animation: "count",
    format: "d",
    theme: "digital"
  };
  configuration2 = {
    animation: "count",
    format: "( ddd),dd",
    theme: "car"
  };
  configuration3 = {
    animation: "count",
    format: "( ddd),dd",
    theme: "train-station"
  };

  constructor(
    private data: DataManagement,
    private router: Router,
    private translator: TranslateService
  ) {}

  ngOnInit() {
    this.type = this.router.url.split("/")[2];
    this.stats = this.getStatistics();
  }

  ngAfterViewInit() {
    if (this.type === "tripsByMonth") {
      this.numberOfTrips = this.stats.numberOfTrips;
      this.loadChart1();
    }
    if (this.type === "publicVsPrivate") {
      this.numberOfTrips = this.stats.numberOfTrips;
      this.percentagePrivateTrips = this.stats.percentagePrivateTrips;
      this.percentagePublicTrips = this.stats.percentagePublicTrips;
      this.ratioOfPrivateTrips = this.stats.ratioOfPrivateTrips;
      this.loadChart2();
    }
    if (this.type === "applicationsPerTrip") {
      this.avgAppsPerTrip = this.stats.avgAppsPerTrip;
    }
    if (this.type === "usersByGender") {
      this.numberOfUsers = this.stats.numberOfUsers;
      this.percentageMen = this.stats.percentageMen;
      this.percentageWomen = this.stats.percentageWomen;
      this.percentageNonBinary = this.stats.percentageNonBinary;
      this.loadChart3();
    }
    if (this.type === "premiumUsers") {
      this.numberOfUsers = this.stats.numberOfUsers;
      this.percentagePremiumUsers = this.stats.percentagePremiumUsers;
      this.percentageNonPremiumUsers = this.stats.percentageNonPremiumUsers;
      this.premiumUsersRatio = this.stats.premiumUsersRatio;
      this.loadChart4();
    }
    if (this.type === "activeVsInactive") {
      this.numberOfUsers = this.stats.numberOfUsers;
      this.percentageActiveUsers = this.stats.percentageActiveUsers;
      this.percentageDeletedUsers = this.stats.percentageDeletedUsers;
      this.activeUsersRatio = this.stats.activeUsersRatio;
      this.loadChart5();
    }
    if (this.type === "usersMetrics") {
      this.avgTripsPerUser = this.stats.avgTripsPerUser;
      this.avgLanguagesPerUser = this.stats.avgLanguagesPerUser;
      this.avgRatingPerUser = this.stats.avgRatingPerUser;
    }
  }

  private loadChart1() {
    const labels =
      this.translator.currentLang === "en"
        ? [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
          ]
        : [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre"
          ];
    const label =
      this.translator.currentLang === "en"
        ? "Number of trips"
        : "Número de viajes";

    this.barChart = new Chart(this.barCanvas.nativeElement, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: label,
            data: [
              this.stats.numberOfTripsJanuary,
              this.stats.numberOfTripsFebruary,
              this.stats.numberOfTripsMarch,
              this.stats.numberOfTripsApril,
              this.stats.numberOfTripsMay,
              this.stats.numberOfTripsJune,
              this.stats.numberOfTripsJuly,
              this.stats.numberOfTripsAugust,
              this.stats.numberOfTripsSeptember,
              this.stats.numberOfTripsOctober,
              this.stats.numberOfTripsNovember,
              this.stats.numberOfTripsDecember
            ],
            backgroundColor: [
              "rgba(0, 72, 255, 0.2)",
              "rgba(201, 188, 156, 0.2)",
              "rgba(195, 96, 96, 0.2)",
              "rgba(194, 147, 189, 0.2)",
              "rgba(177, 231, 251, 0.2)",
              "rgba(244, 235, 139, 0.2)",
              "rgba(251, 149, 65, 0.2)",
              "rgba(192, 243, 88, 0.2)",
              "rgba(103, 203, 103, 0.2)",
              "rgba(160, 144, 208, 0.2)",
              "rgba(201, 100, 100, 0.2)",
              "rgba(167, 145, 134, 0.2)"
            ],
            borderColor: [
              "rgba(0, 72, 255, 1)",
              "rgba(201, 188, 156, 1)",
              "rgba(195, 96, 96, 1)",
              "rgba(194, 147, 189, 1)",
              "rgba(177, 231, 251, 1)",
              "rgba(244, 235, 139, 1)",
              "rgba(251, 149, 65, 1)",
              "rgba(192, 243, 88, 1)",
              "rgba(103, 203, 103, 1)",
              "rgba(160, 144, 208, 1)",
              "rgba(201, 100, 100, 1)",
              "rgba(167, 145, 134, 1)"
            ],
            borderWidth: 1
          }
        ]
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        }
      }
    });
  }

  private loadChart2() {
    const labels =
      this.translator.currentLang === "en"
        ? ["Public trips", "Private trips"]
        : ["Viajes públicos", "Viajes privados"];

    this.doughnutChart = new Chart(this.doughnutCanvas.nativeElement, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: [
              this.stats.numberOfPublicTrips,
              this.stats.numberOfPrivateTrips
            ],
            backgroundColor: [
              "rgba(88, 196, 74, 0.8)",
              "rgba(227, 43, 43, 0.8)"
            ],
            hoverBackgroundColor: [
              "rgba(88, 196, 74, 1)",
              "rgba(227, 43, 43, 1)"
            ]
          }
        ]
      }
    });
  }

  private loadChart3() {
    const labels =
      this.translator.currentLang === "en"
        ? ["Male", "Female", "Non-binary"]
        : ["Hombres", "Mujeres", "Género no binario"];

    this.doughnutChart = new Chart(this.doughnutCanvas.nativeElement, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: [
              this.stats.numberMen,
              this.stats.numberWomen,
              this.stats.numberNonBinary
            ],
            backgroundColor: [
              "rgba(67, 133, 239, 0.8)",
              "rgba(238, 93, 171, 0.8)",
              "rgba(177, 134, 234, 0.8)"
            ],
            hoverBackgroundColor: [
              "rgba(67, 133, 239, 1)",
              "rgba(238, 93, 171, 1)",
              "rgba(177, 134, 234, 1)"
            ]
          }
        ]
      }
    });
  }

  private loadChart4() {
    const labels =
      this.translator.currentLang === "en"
        ? ["Premium users", "Non-Premium users"]
        : ["Usuarios Premium", "Usuarios no Premium"];

    this.doughnutChart = new Chart(this.doughnutCanvas.nativeElement, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: [
              this.stats.numberOfPremiumUsers,
              this.stats.numberOfNonPremiumUsers
            ],
            backgroundColor: [
              "rgba(230, 218, 51, 0.8)",
              "rgba(146, 141, 135, 0.8)"
            ],
            hoverBackgroundColor: [
              "rgba(230, 218, 51, 1)",
              "rgba(146, 141, 135, 1)"
            ]
          }
        ]
      }
    });
  }

  private loadChart5() {
    const labels =
      this.translator.currentLang === "en"
        ? ["Active users", "Inactive users"]
        : ["Usuarios activos", "Usuarios inactivos"];

    this.doughnutChart = new Chart(this.doughnutCanvas.nativeElement, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: [
              this.stats.numberOfActiveUsers,
              this.stats.numberOfDeletedUsers
            ],
            backgroundColor: [
              "rgba(27, 32, 106, 0.8)",
              "rgba(99, 33, 51, 0.8)"
            ],
            hoverBackgroundColor: [
              "rgba(27, 32, 106, 1)",
              "rgba(99, 33, 51, 1)"
            ]
          }
        ]
      }
    });
  }

  private getStatistics(): void {
    this.data
      .getStatistics()
      .then((object: any) => {
        this.stats = object;
      })
      .catch(error => {});
  }
}
