//
//  ViewController.swift
//  Accel
//
//  Created by Aneesh Jain  on 04/04/19.
//  Copyright © 2019 Aneesh Jain . All rights reserved.
//

import UIKit
import CoreMotion
import MapKit
import CoreLocation
import AWSCognito
import AWSS3

class ViewController: UIViewController, CLLocationManagerDelegate {
    
    let bucketName = "pothole-data-unprocessed"
    var taskArr = [Task]()
    var task: Task!
    
    
    @IBOutlet weak var mapView: MKMapView!
    
    var motionManager = CMMotionManager()
    let mapManager = CLLocationManager()
    
    @IBOutlet weak var time_stamp: UITextField!
    
    @IBOutlet weak var x_acc: UITextField!
    @IBOutlet weak var y_acc: UITextField!
    @IBOutlet weak var z_acc: UITextField!
    
    @IBOutlet weak var x_gyro: UITextField!
    @IBOutlet weak var y_gyro: UITextField!
    @IBOutlet weak var z_gyro: UITextField!
    
    @IBOutlet weak var speed: UILabel!
    
    
    func uploadFile(with resource: String, type: String, filePath: URL){
        let key  = "\(resource).\(type)"
        print(key)
        //let localFilePath = Bundle.main.path(forResource: resource, ofType: type)!
        //let localFileUrl = URL(fileURLWithPath: localFilePath)
        let localFileUrl = filePath
        
        let request = AWSS3TransferManagerUploadRequest()!
        request.bucket = bucketName
        request.key = key
        request.body = localFileUrl
        request.acl = .publicReadWrite
        
        let transferManager = AWSS3TransferManager.default()
        transferManager.upload(request).continueWith(executor: AWSExecutor.mainThread()) { (task) -> Any? in
            if let error = task.error {
                print(error)
            }
            
            if task.result != nil{
                print("Uploaded \(key)")
            }
            
            return nil
        }
        
        
    }
    
    func creatCSV() -> Void {
        let fileName = "Tasks.csv"
        let path = NSURL(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent(fileName)
        //print("PATH: \(path!)")
        var csvText = "time stamp,x_acc,y_acc,z_acc,x_gyro,y_gyro,z_gyro,speed,latitude,longitude\n"
        
        for task in taskArr {
            let newLine = "\(task.time_stamp),\(task.acc_x),\(task.acc_y),\(task.acc_z),\(task.gyr_x),\(task.gyr_y),\(task.gyr_z),\(task.speed),\(task.latitude), \(task.longitude)\n"
            csvText.append(newLine)
        }
        
        do {
            try csvText.write(to: path!, atomically: true, encoding: String.Encoding.utf8)
        } catch {
            print("Failed to create file")
            print("\(error)")
        }
        print(path ?? "not found")
        
        uploadFile(with: "Tasks", type: "csv", filePath: path!)
        
        let vc = UIActivityViewController(activityItems: [path], applicationActivities: [])
        present(vc, animated: true, completion: nil)
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        let location = locations[0]
        let span: MKCoordinateSpan = MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
        let myLocation: CLLocationCoordinate2D = CLLocationCoordinate2DMake(location.coordinate.latitude, location.coordinate.longitude)
        let region:MKCoordinateRegion = MKCoordinateRegion(center: myLocation, span: span)
        mapView.setRegion(region, animated: true)
        self.mapView.showsUserLocation = true
        
        //print("Longitude: \(location.coordinate.longitude), Latitude: \(location.coordinate.latitude)")
        if let speed = mapManager.location?.speed, let latitude = mapManager.location?.coordinate.latitude, let longitude = mapManager.location?.coordinate.longitude {
            //print("\(speed.rounded(toPlaces: 3))")
            self.speed.text = String(speed.rounded(toPlaces: 2))
            self.task?.speed = String(speed.rounded(toPlaces: 2))
            self.task?.latitude = String(latitude)
            self.task?.longitude = String(longitude)
            
        }


    }
    
    @IBAction func start(_ sender: UIButton) {
        
        
        motionManager.accelerometerUpdateInterval = 0.2
        motionManager.gyroUpdateInterval = 0.2


        
        
        motionManager.startGyroUpdates(to: OperationQueue.current!){ (gyro_data, error) in
            if let myGyroData = gyro_data{
                
                let x = myGyroData.rotationRate.x
                let y = myGyroData.rotationRate.y
                let z = myGyroData.rotationRate.z
                
                self.x_gyro.text = String(Double(x).rounded(toPlaces: 2))
                self.y_gyro.text = String(Double(y).rounded(toPlaces: 2))
                self.z_gyro.text = String(Double(z).rounded(toPlaces: 2))
                
                self.task.gyr_x = String(Double(x).rounded(toPlaces: 2))
                self.task.gyr_y = String(Double(y).rounded(toPlaces: 2))
                self.task.gyr_z = String(Double(z).rounded(toPlaces: 2))
                //self.taskArr.append(self.task!)
                //print(self.taskArr.count)
                //print(self.task.acc_x,self.task.acc_y,self.task.acc_z)
                
            }
        }
        motionManager.startAccelerometerUpdates(to: OperationQueue.current!){ (acc_data, error) in
            if let myAccData = acc_data{
                
                let x = myAccData.acceleration.x
                let y = myAccData.acceleration.y
                let z = myAccData.acceleration.z
                //self.time_stamp.text = String(myAccData.timestamp)
                self.x_acc.text = String(Double(x).rounded(toPlaces: 2))
                self.y_acc.text = String(Double(y).rounded(toPlaces: 2))
                self.z_acc.text = String(Double(z).rounded(toPlaces: 2))
                
                
                self.task = Task()
                
                self.task.acc_x = String(Double(x).rounded(toPlaces: 2))
                self.task.acc_y = String(Double(y).rounded(toPlaces: 2))
                self.task.acc_z = String(Double(z).rounded(toPlaces: 2))
                self.task.time_stamp = String(myAccData.timestamp.rounded(toPlaces: 6))
                self.taskArr.append(self.task!)
                //print(self.taskArr.count)
                //print(self.taskArr[self.taskArr.count])
            }
        }
        

        
        return
    }
    
    @IBAction func pause(_ sender: UIButton) {
        motionManager.stopAccelerometerUpdates()
        motionManager.stopGyroUpdates()
       // mapManager.stopUpdatingLocation()
        creatCSV()
        
    }
    @IBAction func reset(_ sender: UIButton) {
        taskArr = [Task]()
        self.x_acc.text = String(0.00)
        self.y_acc.text = String(0.00)
        self.z_acc.text = String(0.00)
        self.x_gyro.text = String(0.00)
        self.y_gyro.text = String(0.00)
        self.z_gyro.text = String(0.00)
        
        //self.time_stamp.text = String(0)
        
    }
    
    

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        let credentialsProvider = AWSCognitoCredentialsProvider(regionType:.APSouth1,
                                                                identityPoolId:"ap-south-1:35944358-2654-4c85-8a49-6c44830cc503")
        
        let configuration = AWSServiceConfiguration(region:.APSouth1, credentialsProvider:credentialsProvider)
        
        AWSServiceManager.default().defaultServiceConfiguration = configuration
        
    }
    
    override func viewDidAppear(_ animated: Bool) {
        mapManager.delegate = self
        mapManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        mapManager.requestWhenInUseAuthorization()
        mapManager.startUpdatingLocation()
        
        
        
//        motionManager.accelerometerUpdateInterval = 0.2
//        motionManager.startAccelerometerUpdates(to: OperationQueue.current!){ (data, error) in
//            if let myData = data{
//
//                let x = myData.acceleration.x
//                let y = myData.acceleration.y
//                let z = myData.acceleration.z
//                self.time_stamp.text = String(myData.timestamp)
//                self.x_acc.text = String(Double(x))
//                self.y_acc.text = String(Double(y))
//                self.z_acc.text = String(Double(z))
//
//            }
//        }
//        return
    }


}

extension Double{
    func rounded(toPlaces places: Int) -> Double{
        let divisor = pow(10.0, Double(places))
        return (self * divisor).rounded() / divisor
    }
}


class Task: NSObject {
    var acc_x: String = ""
    var acc_y: String = ""
    var acc_z: String = ""
    var gyr_x: String = ""
    var gyr_y: String = ""
    var gyr_z: String = ""
    var latitude: String = ""
    var longitude: String = ""
    var speed: String = ""
    var time_stamp: String = ""
}



