import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TripResultsPage } from './trip-results.page';

describe('TripsResultsPage', () => {
  let component: TripResultsPage;
  let fixture: ComponentFixture<TripResultsPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TripResultsPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TripResultsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
