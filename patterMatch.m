function [new_start, data_time, data_seg, time] = patterMatch(ev_value, rhythm_number, use_sample)

    %% use_sample = false
    % Fit computation did not converge:
    % Fitting stopped because the number of iterations or function evaluations exceeded the specified maximum.
    
    % Fit found when optimization terminated:
    
    % General model Gauss4:
    %      f(x) = 
    %               a1*exp(-((x-b1)/c1)^2) + a2*exp(-((x-b2)/c2)^2) + 
    %               a3*exp(-((x-b3)/c3)^2) + a4*exp(-((x-b4)/c4)^2)
    % Coefficients (with 95% confidence bounds):
    %        a1 =       313.2  (278.5, 348)
    %        b1 =      -212.1  (-243.6, -180.5)
    %        c1 =       665.2  (613.3, 717)
    %        a2 =       291.9  (-4.147e+04, 4.206e+04)
    %        b2 =       642.7  (489.8, 795.7)
    %        c2 =       270.8  (-462.4, 1004)
    %        a3 =      -265.1  (-4.205e+04, 4.151e+04)
    %        b3 =       644.6  (515.3, 773.9)
    %        c3 =       261.3  (-432.5, 955.1)
    %        a4 =       300.9  (297.3, 304.6)
    %        b4 =        1090  (1013, 1166)
    %        c4 =        1508  (1344, 1671)
    
    % Goodness of fit:
    %   SSE: 239.8
    %   R-square: 0.9999
    %   Adjusted R-square: 0.9999
    %   RMSE: 0.4013

    %% use_sample = true
    % Fit computation did not converge:
    % Fitting stopped because the number of iterations or function evaluations exceeded the specified maximum.

    % Fit found when optimization terminated:

    % General model Gauss4:
    %      f(x) = 
    %               a1*exp(-((x-b1)/c1)^2) + a2*exp(-((x-b2)/c2)^2) + 
    %               a3*exp(-((x-b3)/c3)^2) + a4*exp(-((x-b4)/c4)^2)
    % Coefficients (with 95% confidence bounds):
    %        a1 =       73.36  (-670.1, 816.8)
    %        b1 =      -1.501  (-17.83, 14.83)
    %        c1 =       5.155  (-7.777, 18.09)
    %        a2 =       327.8  (-1275, 1931)
    %        b2 =      0.9073  (-19.35, 21.16)
    %        c2 =       15.43  (-40.05, 70.9)
    %        a3 =       4.764  (-11.31, 20.84)
    %        b3 =       17.48  (16.43, 18.53)
    %        c3 =       3.738  (-0.2222, 7.699)
    %        a4 =       276.8  (-96.95, 650.6)
    %        b4 =       27.36  (-27.96, 82.68)
    %        c4 =       22.88  (-49.43, 95.19)

    % Goodness of fit:
    %   SSE: 4.544
    %   R-square: 1
    %   Adjusted R-square: 0.9999
    %   RMSE: 0.4891
    
    
    
    
    if (~use_sample)
        time = 1/2302:1/2302:length(ev_value)/2302;

        a1 =       313.2;
        b1 =      -212.1;
        c1 =       665.2;
        a2 =       291.9;
        b2 =       642.7;
        c2 =       270.8;
        a3 =      -265.1;
        b3 =       644.6;
        c3 =       261.3;
        a4 =       300.9;
        b4 =        1090;
        c4 =        1508;

        x = 0:1500;
        L = a1*exp(-((x-b1)/c1).^2) + a2*exp(-((x-b2)/c2).^2) + a3*exp(-((x-b3)/c3).^2) + a4*exp(-((x-b4)/c4).^2);

        times = 1;
        rhythm_times = 5;
    else
        time = 1/2302:1/2302:length(ev_value)/2302;

        a1 =       73.36 ;
        b1 =      -1.501;
        c1 =       5.155 ;
        a2 =       327.8;
        b2 =      0.9073;
        c2 =       15.43  ;
        a3 =       4.764;
        b3 =       17.48;
        c3 =       3.738 ;
        a4 =       276.8;
        b4 =       27.36;
        c4 =       22.88;

        x = 0:30;
        L = a1*exp(-((x-b1)/c1).^2) + a2*exp(-((x-b2)/c2).^2) + a3*exp(-((x-b3)/c3).^2) + a4*exp(-((x-b4)/c4).^2);

        times = 50;
        rhythm_times = 3;
    end

    
    heng = []; zong = [];c = [];
    M1 = []; M2 = []; M2i = []; Mx = [];
    startpoint = []; heng2 = []; zong2 = [];
    startpoint2 =[]; data_seg = []; data_time = [];

    j=1;
    % 计算xcorr值
    for i= 1:100/times:length(ev_value)-1500/times
        heng(j,:) = i:i+1500/times;
        zong = ev_value(heng(j,:));
        c(j,:) = xcorr(L,zong,'normalized');
        j=j+1;
    end

    M1 = max(c,[],2);
    [M2,M2i] = sort(M1);
    Mx = M2i(length(M2)-rhythm_number*rhythm_times:length(M2));

    % 取出比对那一段的开始点
    for ii = 1:length(Mx)
        startpoint(ii,:) = heng(Mx(ii),1);
    end
    startpoint = sort(startpoint);

    avg = [];start_point_avg = [];

    for jj = 1:length(startpoint)
        if isempty(avg) || abs(avg(end) - startpoint(jj)) < 500/times
            avg = [avg, startpoint(jj)];
        else
            start_point_avg = [start_point_avg, round(mean(avg))];
            avg = [];
            avg = [avg, startpoint(jj)];
        end
    end

    if ~isempty(avg)
        start_point_avg = [start_point_avg, round(mean(avg))];
    end

    % 根据起始点，找距离它前后的最小值点，作为真正segmentation的起始点，然后取值
    for iii = 1:length(start_point_avg)
        if start_point_avg(iii)-250/times > 0
            heng2(iii,:) = start_point_avg(iii)-250/times:start_point_avg(iii)+50/times;
        else
            heng2(iii,:) = [ones(1,ceil(301/times) - (start_point_avg(iii)+50/times)),1:start_point_avg(iii)+50/times];
        end
        zong2(iii,:) = ev_value(heng2(iii,:));
    end
    [M3,M3i] = max(zong2,[],2);

    for j = 1:length(start_point_avg)
        startpoint2(:,j) = heng2(j,M3i(j));
    end

    startpoint2 = unique(startpoint2);
    avg = [];new_start = [];

    for jj = 1:length(startpoint2)
        if isempty(avg) || abs(avg(end) - startpoint2(jj)) < 500/times
            avg = [avg, startpoint2(jj)];
        else
            new_start = [new_start, round(mean(avg))];
            avg = [];
            avg = [avg, startpoint2(jj)];
        end
    end

    if ~isempty(avg)
        new_start = [new_start, round(mean(avg))];
    end

    for jj = 1:length(new_start)
        data_seg(jj,:) = ev_value(new_start(jj):new_start(jj)+1500/times);
        data_time(jj,:) = time(new_start(jj):new_start(jj)+1500/times);
    end