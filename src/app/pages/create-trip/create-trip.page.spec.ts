import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateTripPage } from './create-trip.page';

describe('CreateTripPage', () => {
  let component: CreateTripPage;
  let fixture: ComponentFixture<CreateTripPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateTripPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateTripPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
