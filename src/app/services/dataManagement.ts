import { test, User, City, Trip } from './../app.data.model';
import { Injectable } from '@angular/core';
import { RestWS } from './restService';

@Injectable()
export class DataManagement {
  constructor(private restService: RestWS) {}

  public login(credentials): Promise<any> {
    return this.restService
      .login(credentials)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }
  public register(
    username: string,
    password: string,
    email: string,
    first_name: string,
    last_name: string,
    description: string,
    birthdate: string,
    gender: string,
    nationality: string,
    city: string,
    languages: string[],
    interests: string[],
    profilePic,
    discoverPic
  ): Promise<any> {
    return this.restService
      .register(
        username,
        password,
        email,
        first_name,
        last_name,
        description,
        birthdate,
        gender,
        nationality,
        city,
        languages,
        interests,
        profilePic,
        discoverPic
      )
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public getUserLogged(token): Promise<any> {
    return this.restService
      .getUserLogged(token)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  public getUserBy(username, token): Promise<any> {
    return this.restService
      .getUserBy(username, token)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  public hasConnection(): boolean {
    return true;
  }

  public listFriends(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.hasConnection()) {
        return this.restService
          .listFriends()
          .then((data: any) => {
            resolve(data);
          })
          .catch(error => {
            reject('error');
          });
      } else {
        reject('error');
      }
    });
  }

  public listYourTrips(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.hasConnection()) {
        return this.restService
          .listYourTrips()
          .then((data: any) => {
            resolve(data);
          })
          .catch(error => {
            reject('error');
          });
      } else {
        reject('error');
      }
    });
  }

  public listSearchTrips(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.hasConnection()) {
        return this.restService
          .listSearchTrips()
          .then((data: any) => {
            resolve(data);
          })
          .catch(error => {
            reject('error');
          });
      } else {
        reject('error');
      }
    });
  }

  public listMeetYou(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.hasConnection()) {
        return this.restService
          .listMeetYou()
          .then((data: any) => {
            resolve(data);
          })
          .catch(error => {
            reject('error');
          });
      } else {
        reject('error');
      }
    });
  }

  public listDiscover(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.hasConnection()) {
        return this.restService
          .listDiscover()
          .then((data: any) => {
            resolve(data);
          })
          .catch(error => {
            reject('error');
          });
      } else {
        reject('error');
      }
    });
  }

  public createTrip(
    title: string,
    description: string,
    start_date: String,
    end_date: String,
    trip_type: string,
    city: Number,
    userImage
  ): Promise<any> {
    return this.restService
      .createTrip(
        title,
        description,
        start_date,
        end_date,
        trip_type,
        city,
        userImage
      )
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public editTrip(
    id: String,
    title: string,
    description: string,
    start_date: String,
    end_date: String,
    trip_type: string,
    city: Number,
    userImage
  ): Promise<any> {
    return this.restService
      .editTrip(
        id,
        title,
        description,
        start_date,
        end_date,
        trip_type,
        city,
        userImage
      )
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public rate(voted: string, rating: Number): Promise<any> {
    return this.restService
      .rate(voted, rating)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }
  public search(searchKey: string): Promise<any> {
    return this.restService
      .search(searchKey)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public paid(): Promise<any> {
    return this.restService
      .paid()
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public listCities(): Promise<any> {
    return this.restService
      .listCities()
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public listLanguages(): Promise<any> {
    return this.restService
      .listLanguages()
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }
  public listInterests(): Promise<any> {
    return this.restService
      .listInterests()
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public getTripById(id: string): Promise<Trip> {
    return this.restService
      .getTripById(id)
      .then(response => {
        return Promise.resolve(response);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  public sendMessage(
    sender: string,
    receiver: string,
    message: string
  ): Promise<any> {
    return this.restService
      .sendMessage(sender, receiver, message)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public getMessages(senderId: Number, receiverId: Number): Promise<any> {
    return this.restService
      .getMessages(senderId, receiverId)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public resolveFriendRequest(request: string, username: string): Promise<any> {
    return this.restService
      .resolveFriendRequest(request, username)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  public applyForTrip(tripId: string): Promise<any> {
    return this.restService
      .applyForTrip(tripId)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  public sendFriendInvitation(username: string): Promise<any> {
    return this.restService
      .sendFriendInvitation(username)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  public getUserById(id: string): Promise<any> {
    return this.restService
      .getUserById(id)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  public resolveTripApplication(
    request: string,
    applicationId: string
  ): Promise<any> {
    return this.restService
      .resolveTripApplication(request, applicationId)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  public getStatistics(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.hasConnection()) {
        return this.restService
          .getStatistics()
          .then((data: any) => {
            resolve(data);
          })
          .catch(error => {
            reject('error');
          });
      } else {
        reject('error');
      }
    });
  }
}
