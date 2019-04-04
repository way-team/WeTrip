import { Component, OnInit } from '@angular/core';
import { Trip } from 'src/app/app.data.model';
import { ActivatedRoute } from '@angular/router';
import { DataManagement } from 'src/app/services/dataManagement';

@Component({
  selector: 'app-trip-detail',
  templateUrl: './trip-detail.page.html',
  styleUrls: ['./trip-detail.page.scss'],
})
export class TripdetailPage implements OnInit {

  trip: Trip;


  constructor(
    private activatedRoute: ActivatedRoute,
    private dm: DataManagement

  ) {
    const tripId = this.activatedRoute.snapshot.paramMap.get('id');
    this.dm.getTripById(tripId).then(response => {
      this.trip = response;
    }).catch((_) => {

    });
   }

  ngOnInit() {
  }

}
