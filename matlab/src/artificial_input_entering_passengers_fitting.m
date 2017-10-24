%% Entering passengers 

%% Variable modification
% dataset01=table2array(inputdatapassengers01);
% dataset02=table2array(inputdatapassengers02);
% dataset03=table2array(inputdatapassengers03);
% dataset04=table2array(inputdatapassengers04);
% dataset015=table2array(inputdatapassengers015);
% dataset025=table2array(inputdatapassengers025);
% dataset06=table2array(inputdatapassengers06);
%global_validation_dataset=[dataset01;dataset02;dataset03;...
%             dataset04;dataset015;dataset025;dataset06];

%% Fitting
% Poisson fitting for every station 
% for every direction 
% for every period defined in timetable

%NOTE 2 times run one for each direction 
%1st global_validation_dataset(j,1)==0 for direction 1
%2st global_validation_dataset(j,1)==1 for direction 2

% temp=9;
% time_ind=1;
% clear X;
% X=[];
% timetable=[7 9 16 18 21.5];
% for i=1 : 9
%   for time_ind=1:length(timetable) 
%     for j=i :temp : length(global_validation_dataset)
%         %1st condition of if to determine the direction
%         %2nd condition to determine the time
%         if(   global_validation_dataset(j,1)==0 && ...
%         global_validation_dataset(j,3)<= timetable(time_ind) && ...
%         (j) <= length(global_validation_dataset) )
%              
%                   X=[X,global_validation_dataset(j,4)];
%         end
%     end  
%     lambdas_direction_1(time_ind,i)=poissfit(X);
%     clear X;
%     X=[];
%   end
% end
% 
% clear i j X temp time_ind;
% 
%% transforming the dataset to be the same with the one of the real data
% 1st merging the 2 directions
artificial_labdas_pin= [lambdas_direction_1,lambdas_direction_2];
        
% divide every hour to quarters
%
quarters=[4 8 28 8 14];
artificial_lambdas_pin_final=[];

for i=1:5
    for j=1:18
        artificial_labdas_pin_final(i,j)=(artificial_labdas_pin(i,j)*15 )/(quarters(i)*15);
    end
end

clear i j;



artificial_lambdas_pin_final2=[];
for i=1:5
    for j=1:(quarters(i))
    artificial_lambdas_pin_final2=[artificial_lambdas_pin_final2;
                                artificial_labdas_pin_final(i,:)];
    end  

end

clear i j quarters;





