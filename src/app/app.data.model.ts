
export class UserProfile {
  user: User;
  email: string;
  first_name: string;
  last_name: string;
  description: string;
  birthdate: string;
  city: string;
  nationality: string;
  photo: string;
  discoverPhoto: string;
  averageRate: Number;
  numRate: Number;
  isPremium: boolean;
  status: boolean;
  gender: string;
  language: string;
}

export class Trip {
  id: Number;
  title: String;
  description: String;
  startDate: Date;
  endDate: Date;
  tripType: String;
  image: String;
  status: Boolean;
  user_id: Number;
}

export class City {
  id: Number;
  name: String;
}


export class User {
  id: Number;
  username: string;
}

export class test {
  count: string;
  next: string;
  previous: string;
  results: User[];
}

